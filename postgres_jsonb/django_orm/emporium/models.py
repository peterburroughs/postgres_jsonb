from django.db import models
from django.contrib.postgres.fields.jsonb import JSONField


class Supplier(models.Model):
    name = models.CharField(max_length=50)
    tax_id = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Bargain(models.Model):
    sku = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,
                                 db_index=True)
    info = JSONField(db_index=True)  # This will create a btree index, not GIN

    def __str__(self):
        return self.sku

    @property
    def description(self):
        return self.info.get('description', '')

    @property
    def sale_price(self):
        return self.info.get('sale_price', '')

    @property
    def acquire_cost(self):
        return self.info.get('acquire_cost', '')

    @property
    def color(self):
        return self.info.get('color', '')
