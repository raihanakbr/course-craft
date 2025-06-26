from django.core.management.base import BaseCommand
from django.utils import timezone
from payment.models import UserSubscription


class Command(BaseCommand):
    help = 'Check and expire subscriptions that have passed their end date'

    def handle(self, *args, **options):
        self.stdout.write('Checking for expired subscriptions...')
        
        # Find active subscriptions that have passed their end date
        expired_subscriptions = UserSubscription.objects.filter(
            status='ACTIVE',
            end_date__lt=timezone.now()
        )
        
        count = 0
        for subscription in expired_subscriptions:
            subscription.expire_subscription()
            count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'Expired subscription for {subscription.user.username} - {subscription.subscription_plan.display_name}'
                )
            )
        
        if count == 0:
            self.stdout.write('No expired subscriptions found.')
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully expired {count} subscription(s).')
            )
