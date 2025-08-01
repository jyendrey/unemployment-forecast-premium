#!/usr/bin/env python3
"""
Alert Management System for Interactive Brokers Dashboard
=========================================================

Handles real-time alerts, notifications, and escalation for the
unemployment forecasting system.

Features:
- Real-time alert generation
- Email notifications
- Alert history and analytics
- Escalation rules
- Performance monitoring
"""

import smtplib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

class AlertManager:
    """
    Comprehensive alert management for unemployment forecasting system
    """
    
    def __init__(self):
        # Configuration
        self.recipient_email = "jyendrey@interactivebrokers.com"
        self.system_name = "Labor Market Intelligence Dashboard"
        self.alert_history = []
        self.alert_rules = self._initialize_alert_rules()
        
        # Alert state tracking
        self.active_alerts = {}
        self.alert_counts = {'info': 0, 'warning': 0, 'error': 0, 'critical': 0}
        self.last_notification_time = {}
        
        # Performance tracking
        self.forecast_accuracy_threshold = 95.0
        self.confidence_threshold = 98.0
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _initialize_alert_rules(self) -> Dict:
        """Initialize comprehensive alert rules"""
        return {
            'forecast_confidence_drop': {
                'threshold': 95.0,
                'severity': 'warning',
                'cooldown_minutes': 60,
                'escalation_threshold': 90.0,
                'description': 'Model confidence below target threshold'
            },
            'forecast_accuracy_decline': {
                'threshold': 95.0,
                'severity': 'warning',
                'cooldown_minutes': 120,
                'escalation_threshold': 90.0,
                'description': 'Historical forecast accuracy declining'
            },
            'labor_force_participation_change': {
                'threshold': 0.15,
                'severity': 'warning',
                'cooldown_minutes': 30,
                'escalation_threshold': 0.25,
                'description': 'Significant labor force participation change'
            },
            'claims_surge': {
                'threshold': 350000,
                'severity': 'warning',
                'cooldown_minutes': 60,
                'escalation_threshold': 400000,
                'description': 'Initial jobless claims above normal levels'
            },
            'api_failure': {
                'threshold': 1,
                'severity': 'error',
                'cooldown_minutes': 15,
                'escalation_threshold': 2,
                'description': 'API data source failure'
            },
            'data_quality_degradation': {
                'threshold': 0.8,
                'severity': 'warning',
                'cooldown_minutes': 45,
                'escalation_threshold': 0.6,
                'description': 'Overall data quality below acceptable levels'
            },
            'forecast_error_large': {
                'threshold': 0.2,
                'severity': 'error',
                'cooldown_minutes': 120,
                'escalation_threshold': 0.3,
                'description': 'Forecast error exceeds tolerance'
            },
            'system_performance': {
                'threshold': 5.0,  # seconds
                'severity': 'warning',
                'cooldown_minutes': 30,
                'escalation_threshold': 10.0,
                'description': 'System response time degradation'
            }
        }
    
    def process_forecast_alert(self, forecast_data: Dict) -> List[Dict]:
        """Process alerts from forecast data"""
        alerts = []
        
        try:
            # Check confidence levels
            for forecast in forecast_data.get('forecasts', []):
                confidence = forecast.get('confidence', 100)
                
                if confidence < self.alert_rules['forecast_confidence_drop']['threshold']:
                    alert = self._create_alert(
                        'forecast_confidence_drop',
                        f"Forecast confidence for {forecast['month']} dropped to {confidence}%",
                        {'confidence': confidence, 'month': forecast['month']},
                        'critical' if confidence < self.alert_rules['forecast_confidence_drop']['escalation_threshold'] else 'warning'
                    )
                    alerts.append(alert)
                
                # Check error margins
                error_margin = forecast.get('error_margin', 0)
                if error_margin > self.alert_rules['forecast_error_large']['threshold']:
                    alert = self._create_alert(
                        'forecast_error_large',
                        f"Forecast error margin for {forecast['month']}: ±{error_margin:.2f}%",
                        {'error_margin': error_margin, 'month': forecast['month']},
                        'critical' if error_margin > self.alert_rules['forecast_error_large']['escalation_threshold'] else 'error'
                    )
                    alerts.append(alert)
            
            # Check overall system performance
            system_performance = forecast_data.get('system_performance', {})
            overall_confidence = system_performance.get('average_confidence', 100)
            
            if overall_confidence < self.confidence_threshold:
                alert = self._create_alert(
                    'forecast_confidence_drop',
                    f"Overall system confidence: {overall_confidence:.1f}% (Target: {self.confidence_threshold}%)",
                    {'overall_confidence': overall_confidence},
                    'critical' if overall_confidence < 95 else 'warning'
                )
                alerts.append(alert)
        
        except Exception as e:
            alert = self._create_alert(
                'system_performance',
                f"Error processing forecast alerts: {str(e)}",
                {'error': str(e)},
                'error'
            )
            alerts.append(alert)
        
        return alerts
    
    def process_data_alert(self, data_quality: Dict, real_time_data: Dict) -> List[Dict]:
        """Process alerts from data quality and real-time data"""
        alerts = []
        
        try:
            # Data quality alerts
            quality_score = data_quality.get('overall_score', 1.0)
            
            if quality_score < self.alert_rules['data_quality_degradation']['threshold']:
                severity = 'critical' if quality_score < self.alert_rules['data_quality_degradation']['escalation_threshold'] else 'warning'
                alert = self._create_alert(
                    'data_quality_degradation',
                    f"Data quality degraded to {quality_score:.1%} ({data_quality.get('apis_working', 0)}/{data_quality.get('total_apis', 3)} APIs working)",
                    {'quality_score': quality_score, 'apis_working': data_quality.get('apis_working', 0)},
                    severity
                )
                alerts.append(alert)
            
            # API failure alerts
            api_status = real_time_data.get('api_status', {})
            failed_apis = [api for api, status in api_status.items() if not status]
            
            if failed_apis:
                for api in failed_apis:
                    alert = self._create_alert(
                        'api_failure',
                        f"{api.upper()} API connection failed",
                        {'failed_api': api},
                        'critical' if len(failed_apis) > 1 else 'error'
                    )
                    alerts.append(alert)
            
            # Labor force participation alerts
            lfp_data = real_time_data.get('labor_force_participation', {})
            participation_change = lfp_data.get('participation_rate', {}).get('recent_change', 0)
            
            if abs(participation_change) > self.alert_rules['labor_force_participation_change']['threshold']:
                severity = 'critical' if abs(participation_change) > self.alert_rules['labor_force_participation_change']['escalation_threshold'] else 'warning'
                direction = "declined" if participation_change < 0 else "increased"
                
                alert = self._create_alert(
                    'labor_force_participation_change',
                    f"Labor force participation {direction} by {abs(participation_change):.2f}% (critical indicator)",
                    {'participation_change': participation_change},
                    severity
                )
                alerts.append(alert)
            
            # Claims surge alerts
            claims_data = real_time_data.get('weekly_claims', {})
            initial_claims = claims_data.get('initial_claims', {}).get('current', 0)
            
            if initial_claims > self.alert_rules['claims_surge']['threshold']:
                severity = 'critical' if initial_claims > self.alert_rules['claims_surge']['escalation_threshold'] else 'warning'
                
                alert = self._create_alert(
                    'claims_surge',
                    f"Initial jobless claims surge: {initial_claims:,.0f} (threshold: {self.alert_rules['claims_surge']['threshold']:,.0f})",
                    {'initial_claims': initial_claims},
                    severity
                )
                alerts.append(alert)
        
        except Exception as e:
            alert = self._create_alert(
                'system_performance',
                f"Error processing data alerts: {str(e)}",
                {'error': str(e)},
                'error'
            )
            alerts.append(alert)
        
        return alerts
    
    def _create_alert(self, alert_type: str, message: str, data: Dict, severity: str) -> Dict:
        """Create standardized alert object"""
        alert_id = f"{alert_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        alert = {
            'id': alert_id,
            'type': alert_type,
            'severity': severity,
            'message': message,
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'acknowledged': False,
            'escalated': severity in ['critical'],
            'rule': self.alert_rules.get(alert_type, {})
        }
        
        return alert
    
    def should_send_notification(self, alert: Dict) -> bool:
        """Determine if notification should be sent based on cooldown rules"""
        alert_type = alert['type']
        rule = self.alert_rules.get(alert_type, {})
        cooldown_minutes = rule.get('cooldown_minutes', 30)
        
        # Check last notification time for this alert type
        last_time = self.last_notification_time.get(alert_type)
        
        if not last_time:
            return True
        
        time_diff = (datetime.now() - last_time).total_seconds() / 60
        return time_diff >= cooldown_minutes
    
    def send_email_alert(self, alert: Dict) -> bool:
        """Send email notification for critical alerts"""
        try:
            # For demo purposes, we'll log the email content
            # In production, you'd configure SMTP settings
            
            subject = f"🚨 {self.system_name} Alert: {alert['type'].replace('_', ' ').title()}"
            
            body = f"""
            ALERT NOTIFICATION - Labor Market Intelligence Dashboard
            =====================================================
            
            Severity: {alert['severity'].upper()}
            Alert Type: {alert['type'].replace('_', ' ').title()}
            Timestamp: {alert['timestamp']}
            
            Message:
            {alert['message']}
            
            Additional Data:
            {json.dumps(alert['data'], indent=2)}
            
            Alert Rule:
            - Threshold: {alert['rule'].get('threshold', 'N/A')}
            - Escalation: {alert['rule'].get('escalation_threshold', 'N/A')}
            - Description: {alert['rule'].get('description', 'N/A')}
            
            System Status:
            - Dashboard: https://unemployment-forecast-premium.streamlit.app
            - Alert ID: {alert['id']}
            
            This is an automated alert from the Interactive Brokers
            Labor Market Intelligence Dashboard.
            
            ---
            Interactive Brokers | Labor Market Intelligence
            """
            
            # Log the email (in production, send via SMTP)
            self.logger.info(f"EMAIL ALERT SENT to {self.recipient_email}")
            self.logger.info(f"Subject: {subject}")
            self.logger.info(f"Body preview: {body[:200]}...")
            
            # Update notification time
            self.last_notification_time[alert['type']] = datetime.now()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {str(e)}")
            return False
    
    def process_alerts(self, alerts: List[Dict]) -> Dict:
        """Process a batch of alerts and manage notifications"""
        processed_alerts = []
        notifications_sent = 0
        
        for alert in alerts:
            # Add to history
            self.alert_history.append(alert)
            
            # Update counters
            severity = alert['severity']
            if severity in self.alert_counts:
                self.alert_counts[severity] += 1
            
            # Determine if notification should be sent
            if self.should_send_notification(alert):
                if alert['severity'] in ['critical', 'error']:
                    if self.send_email_alert(alert):
                        notifications_sent += 1
                        alert['notification_sent'] = True
                    else:
                        alert['notification_sent'] = False
                else:
                    # For warning/info alerts, just log
                    self.logger.info(f"Alert logged: {alert['message']}")
                    alert['notification_sent'] = False
            else:
                alert['notification_sent'] = False
                alert['notification_suppressed'] = True
            
            # Add to active alerts if not acknowledged
            if not alert['acknowledged']:
                self.active_alerts[alert['id']] = alert
            
            processed_alerts.append(alert)
        
        return {
            'processed_count': len(processed_alerts),
            'notifications_sent': notifications_sent,
            'active_alerts_count': len(self.active_alerts),
            'alerts': processed_alerts
        }
    
    def get_alert_summary(self) -> Dict:
        """Get comprehensive alert summary for dashboard"""
        now = datetime.now()
        
        # Recent alerts (last 24 hours)
        recent_threshold = now - timedelta(hours=24)
        recent_alerts = [
            alert for alert in self.alert_history 
            if datetime.fromisoformat(alert['timestamp']) > recent_threshold
        ]
        
        # Active critical alerts
        critical_alerts = [
            alert for alert in self.active_alerts.values() 
            if alert['severity'] == 'critical' and not alert['acknowledged']
        ]
        
        # Alert trends
        alert_trends = {}
        for period in ['1h', '6h', '24h']:
            if period == '1h':
                threshold = now - timedelta(hours=1)
            elif period == '6h':
                threshold = now - timedelta(hours=6)
            else:
                threshold = now - timedelta(hours=24)
            
            period_alerts = [
                alert for alert in self.alert_history 
                if datetime.fromisoformat(alert['timestamp']) > threshold
            ]
            
            alert_trends[period] = {
                'total': len(period_alerts),
                'critical': len([a for a in period_alerts if a['severity'] == 'critical']),
                'error': len([a for a in period_alerts if a['severity'] == 'error']),
                'warning': len([a for a in period_alerts if a['severity'] == 'warning'])
            }
        
        return {
            'active_alerts': len(self.active_alerts),
            'critical_alerts': len(critical_alerts),
            'recent_alerts_24h': len(recent_alerts),
            'alert_trends': alert_trends,
            'total_alerts_all_time': len(self.alert_history),
            'alert_counts': self.alert_counts.copy(),
            'latest_alerts': recent_alerts[-5:] if recent_alerts else [],
            'system_health': 'healthy' if len(critical_alerts) == 0 else 'degraded',
            'last_update': now.isoformat()
        }
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an active alert"""
        if alert_id in self.active_alerts:
            self.active_alerts[alert_id]['acknowledged'] = True
            self.active_alerts[alert_id]['acknowledged_time'] = datetime.now().isoformat()
            
            # Remove from active alerts
            del self.active_alerts[alert_id]
            
            self.logger.info(f"Alert {alert_id} acknowledged")
            return True
        
        return False
    
    def get_alert_history(self, hours: int = 24) -> List[Dict]:
        """Get alert history for specified time period"""
        threshold = datetime.now() - timedelta(hours=hours)
        
        return [
            alert for alert in self.alert_history 
            if datetime.fromisoformat(alert['timestamp']) > threshold
        ]
    
    def clear_old_alerts(self, days: int = 30) -> int:
        """Clear alert history older than specified days"""
        threshold = datetime.now() - timedelta(days=days)
        
        original_count = len(self.alert_history)
        self.alert_history = [
            alert for alert in self.alert_history 
            if datetime.fromisoformat(alert['timestamp']) > threshold
        ]
        
        cleared_count = original_count - len(self.alert_history)
        self.logger.info(f"Cleared {cleared_count} old alerts (older than {days} days)")
        
        return cleared_count

if __name__ == "__main__":
    # Test the alert system
    alert_manager = AlertManager()
    
    print("Testing Alert Management System...")
    print("=" * 50)
    
    # Simulate some alerts
    test_alerts = [
        alert_manager._create_alert(
            'forecast_confidence_drop',
            'Test confidence drop alert',
            {'confidence': 94.5},
            'warning'
        ),
        alert_manager._create_alert(
            'labor_force_participation_change',
            'Test participation change alert',
            {'participation_change': -0.20},
            'critical'
        )
    ]
    
    # Process alerts
    result = alert_manager.process_alerts(test_alerts)
    
    print(f"Processed {result['processed_count']} alerts")
    print(f"Sent {result['notifications_sent']} notifications")
    print(f"Active alerts: {result['active_alerts_count']}")
    
    # Get summary
    summary = alert_manager.get_alert_summary()
    print(f"\nSystem Health: {summary['system_health']}")
    print(f"Critical Alerts: {summary['critical_alerts']}")
    print(f"Recent Alerts (24h): {summary['recent_alerts_24h']}")
