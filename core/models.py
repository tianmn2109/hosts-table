from django.db import models


class Raw(models.Model):
    ip = models.CharField(max_length=255)
    updated = models.DateTimeField(auto_now=True)
    data = models.TextField()


class Host(models.Model):
    uuid = models.CharField(max_length=255, unique=True)
    sn = models.CharField(max_length=255, db_index=True)
    maintainer = models.CharField(max_length=255, db_index=True)
    machinepos = models.CharField(max_length=255,db_index=True)
    badgenumber = models.CharField(max_length=255,db_index=True)

    hostname = models.CharField(max_length=255, db_index=True)
    ip = models.CharField(max_length=255, db_index=True)

    cpus = models.CharField(max_length=255)
    memory = models.CharField(max_length=255)
    slots = models.CharField(max_length=255)
    disk = models.CharField(max_length=255)

    mac = models.CharField(max_length=255)
    osinfo = models.CharField(max_length=255)

    updated = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    host = models.ForeignKey(Host)
    updated = models.DateTimeField(auto_now=True)
    comment = models.TextField()

class Update(models.Model):
    uuid = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    changetime = models.DateTimeField(auto_now=True)
    operation = models.CharField(max_length=255,db_index=True)
