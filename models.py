from django.db import models


class YearAnalytics(models.Model):
    year = models.IntegerField(primary_key=True)
    salary = models.FloatField()
    count = models.IntegerField()
    salary_vac = models.FloatField()
    count_vac = models.IntegerField()

    def __str__(self):
        return str(self.year)
    
    class Meta:
        db_table = 'year_analytics'


class AreaSalary(models.Model):
    area = models.CharField(max_length=20, primary_key=True)
    salary = models.FloatField()

    def __str__(self):
        return self.area
    
    class Meta:
        db_table = 'area_salary'


class AreaPart(models.Model):
    area = models.CharField(max_length=20, primary_key=True)
    part = models.FloatField()

    def __str__(self):
        return self.area
    
    class Meta:
        db_table = 'area_part'


class AreaSalaryVacancy(models.Model):
    area = models.CharField(max_length=20, primary_key=True)
    salary = models.FloatField()

    def __str__(self):
        return self.area
    
    class Meta:
        db_table = 'area_salary_vacancy'


class AreaPartVacancy(models.Model):
    area = models.CharField(max_length=20, primary_key=True)
    part = models.FloatField()

    def __str__(self):
        return self.area
    
    class Meta:
        db_table = 'area_part_vacancy'


class YearSkills(models.Model):
    year = models.IntegerField(primary_key=True)
    skill1 = models.CharField(max_length=20)
    skill2 = models.CharField(max_length=20)
    skill3 = models.CharField(max_length=20)
    skill4 = models.CharField(max_length=20)
    skill5 = models.CharField(max_length=20)
    skill6 = models.CharField(max_length=20)
    skill7 = models.CharField(max_length=20)
    skill8 = models.CharField(max_length=20)
    skill9 = models.CharField(max_length=20)
    skill10 = models.CharField(max_length=20)
    skill11 = models.CharField(max_length=20)
    skill12 = models.CharField(max_length=20)
    skill13 = models.CharField(max_length=20)
    skill14 = models.CharField(max_length=20)
    skill15 = models.CharField(max_length=20)
    skill16 = models.CharField(max_length=20)
    skill17 = models.CharField(max_length=20)
    skill18 = models.CharField(max_length=20)
    skill19 = models.CharField(max_length=20)
    skill20 = models.CharField(max_length=20)

    def __str__(self):
        return str(self.year)
    
    class Meta:
        db_table = 'year_skills'


class YearSkillsVacancy(models.Model):
    year = models.IntegerField(primary_key=True)
    skill1 = models.CharField(max_length=20)
    skill2 = models.CharField(max_length=20)
    skill3 = models.CharField(max_length=20)
    skill4 = models.CharField(max_length=20)
    skill5 = models.CharField(max_length=20)
    skill6 = models.CharField(max_length=20)
    skill7 = models.CharField(max_length=20)
    skill8 = models.CharField(max_length=20)
    skill9 = models.CharField(max_length=20)
    skill10 = models.CharField(max_length=20)
    skill11 = models.CharField(max_length=20)
    skill12 = models.CharField(max_length=20)
    skill13 = models.CharField(max_length=20)
    skill14 = models.CharField(max_length=20)
    skill15 = models.CharField(max_length=20)
    skill16 = models.CharField(max_length=20)
    skill17 = models.CharField(max_length=20)
    skill18 = models.CharField(max_length=20)
    skill19 = models.CharField(max_length=20)
    skill20 = models.CharField(max_length=20)

    def __str__(self):
        return str(self.year)
    
    class Meta:
        db_table = 'year_skills_vacancy'


class ImageModel(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    models.URLField()