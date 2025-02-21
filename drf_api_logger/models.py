from django.db import models

from drf_api_logger.utils import database_log_enabled


if database_log_enabled():
    """
    Load models only if DRF_API_LOGGER_DATABASE is True
    """
    class BaseModel(models.Model):
        id = models.BigAutoField(primary_key=True)

        added_on = models.DateTimeField()

        def __str__(self):
            return str(self.id)

        class Meta:
            abstract = True
            ordering = ('-added_on',)


    class APILogsModel(BaseModel):
        api = models.CharField(max_length=1024, help_text='API URL')
        headers = models.TextField()
        body = models.TextField()
        method = models.CharField(max_length=10, db_index=True)
        client_ip_address = models.CharField(max_length=50)
        response = models.TextField()
        status_code = models.PositiveSmallIntegerField(help_text='Response status code', db_index=True)
        execution_time = models.DecimalField(decimal_places=5, max_digits=8,
                                             help_text='Server execution time (Not complete response time.)')

        external_lookup_id = models.CharField(max_length=512, default=None, null=True, blank=True)
        business_id = models.CharField(max_length=512, default=None, null=True, blank=True, db_index=True)
        user_id = models.CharField(max_length=512, default=None, null=True, blank=True, db_index=True)
        apikey_id = models.CharField(max_length=512, default=None, null=True, blank=True, db_index=True)
        data = models.JSONField(default=dict, blank=True)

        def __str__(self):
            if self.business_id:
                return f"[BID:{str(self.business_id)}] self.api"
            return self.api

        class Meta:
            db_table = 'drf_api_logs'
            verbose_name = 'API Log'
            verbose_name_plural = 'API Logs'
