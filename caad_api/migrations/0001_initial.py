# Generated by Django 4.2.4 on 2023-09-14 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccomodationProforma',
            fields=[
                ('ac_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_of_application', models.DateField()),
                ('security_and_police_proforma', models.BooleanField()),
                ('application_status', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('challan_no', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
            ],
            options={
                'db_table': 'accomodation_proforma',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AccomodationType',
            fields=[
                ('accomodation_id', models.AutoField(primary_key=True, serialize=False)),
                ('accm_description', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=150, null=True)),
            ],
            options={
                'db_table': 'accomodation_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=255)),
                ('codename', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=150, unique=True)),
                ('first_name', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=150)),
                ('last_name', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=150)),
                ('email', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CaadAccomodationVerification',
            fields=[
                ('caad_hr3_id', models.AutoField(primary_key=True, serialize=False)),
                ('registration_entries', models.BooleanField(blank=True, null=True)),
                ('police_verification', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'caad_accomodation_verification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CaadClearanceVerification',
            fields=[
                ('caad_clearance_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'caad_clearance_verification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CaadEvaluationVerification',
            fields=[
                ('caad_evaluation_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'caad_evaluation_verification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CaadExtensionVerification',
            fields=[
                ('caad_extension_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'caad_extension_verification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CaadIdentityVerification',
            fields=[
                ('caad_identity_id', models.AutoField(db_column='CAAD_identity_id', primary_key=True, serialize=False)),
                ('university_type', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('security_particular_proforma', models.BooleanField(blank=True, null=True)),
                ('police_verification_proforma', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'caad_identity_verification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CaadLatesittingVerification',
            fields=[
                ('caad_latesitting_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'caad_latesitting_verification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CaadRegistrationVerification',
            fields=[
                ('caad_registration_verification', models.AutoField(primary_key=True, serialize=False)),
                ('academic_record_acceptable', models.BooleanField(blank=True, null=True)),
                ('financial_matter_involve', models.BooleanField(blank=True, null=True)),
                ('applicant_applicable', models.BooleanField(blank=True, null=True)),
                ('funds_available', models.BooleanField(blank=True, null=True)),
                ('applicant_considered', models.BooleanField(blank=True, null=True)),
                ('tors_issue_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'caad_registration_verification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CaadTransportVerification',
            fields=[
                ('transport_confirmation_id', models.AutoField(primary_key=True, serialize=False)),
                ('transport_availability', models.BooleanField(blank=True, null=True)),
                ('vehicle_reg_no', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('vehicle_type', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('remarks', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=100, null=True)),
                ('confirmation_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'caad_transport_verification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ClearancePerforma',
            fields=[
                ('clearance_id', models.AutoField(primary_key=True, serialize=False)),
                ('reason_to_leave', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=100, null=True)),
                ('application_status', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
            ],
            options={
                'db_table': 'clearance_performa',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', null=True)),
                ('object_repr', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=100)),
                ('model', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=255)),
                ('name', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('doc_id', models.IntegerField(primary_key=True, serialize=False)),
                ('doc_name', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('required', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'documents',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentsUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaddoc_id', models.IntegerField(db_column='uploadDoc_id')),
                ('image', models.BinaryField(blank=True, max_length='max', null=True)),
            ],
            options={
                'db_table': 'documents_upload',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EvaluationProforma',
            fields=[
                ('evaluation_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_of_submission', models.DateField(blank=True, null=True)),
                ('research_status', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('research_title', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('research_summary', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=250, null=True)),
            ],
            options={
                'db_table': 'evaluation_proforma',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExtensionProforma',
            fields=[
                ('extension_form_id', models.AutoField(primary_key=True, serialize=False)),
                ('approval_date', models.DateField(blank=True, null=True)),
                ('reason_for_extension', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=150)),
                ('reqperiod_ex_startdate', models.DateField()),
                ('reqperiod_ex_enddate', models.DateField()),
                ('accomodation', models.BooleanField()),
                ('transport', models.BooleanField()),
                ('application_status', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
            ],
            options={
                'db_table': 'extension_proforma',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HostedresearcherCategory',
            fields=[
                ('category_id', models.IntegerField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
            ],
            options={
                'db_table': 'hostedresearcher_category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='IdentitycardProforma',
            fields=[
                ('identity_id', models.AutoField(primary_key=True, serialize=False)),
                ('identity_apply_date', models.DateField(blank=True, null=True)),
                ('registration_date', models.DateField(blank=True, null=True)),
                ('registration_receipt_number', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('blood_group', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('identification_mark', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('application_status', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
            ],
            options={
                'db_table': 'identitycard_proforma',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Internships',
            fields=[
                ('internship_id', models.AutoField(primary_key=True, serialize=False)),
                ('proposed_research_area', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('proposed_research_start_time', models.DateField(blank=True, null=True)),
                ('proposed_research_end_time', models.DateField(blank=True, null=True)),
                ('accomodation_required', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=10, null=True)),
                ('accomodation_start_time', models.DateField(blank=True, null=True)),
                ('accomodation_end_time', models.DateField(blank=True, null=True)),
                ('application_status', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('ncp_employee_id', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('ncp_assigned_regno', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('proposed_research_department', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('is_supervisor_from_ncp', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=10, null=True)),
                ('is_cosupervisor_from_ncp', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=10, null=True)),
                ('consulted_date_of_ncp_supervisor', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'internships',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ItDeptLogin',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('email_acc', models.BooleanField(blank=True, null=True)),
                ('window_login_acc', models.BooleanField(blank=True, null=True)),
                ('all_user_mailing_list', models.BooleanField(blank=True, null=True)),
                ('linux_acc', models.BooleanField(blank=True, null=True)),
                ('print_quota', models.BooleanField(blank=True, null=True)),
                ('department_mailing_list', models.BooleanField(blank=True, null=True)),
                ('vpn_account', models.BooleanField(blank=True, null=True)),
                ('record_update', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'it_dept_login',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LateSittingProforma',
            fields=[
                ('latesit_id', models.AutoField(primary_key=True, serialize=False)),
                ('late_performa_submitdate', models.DateField(blank=True, null=True)),
                ('latesitting_reason', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=150, null=True)),
                ('workarea_during_latework', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('lab_contact_no', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('latesitting_startdate', models.DateField(blank=True, null=True)),
                ('latesitting_enddate', models.DateField(blank=True, null=True)),
                ('emergency_contact_name', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('emergency_contact_number', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('emergency_contact_landline', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('attendant_during_latework', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('recommended_by_supervisor', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'late_sitting_proforma',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LoginProforma',
            fields=[
                ('login_form_id', models.AutoField(primary_key=True, serialize=False)),
                ('building', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('floor', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('room_no', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('window_login_account', models.BooleanField(blank=True, null=True)),
                ('email_account', models.BooleanField(blank=True, null=True)),
                ('print_quota', models.BooleanField()),
                ('linux_account', models.BooleanField(blank=True, null=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('mac_address', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('purpose_it_account', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', db_column='purpose_IT_account', max_length=150, null=True)),
                ('application_status', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
            ],
            options={
                'db_table': 'login_proforma',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NcpAccomodationApproval',
            fields=[
                ('ncp_allotted_id', models.AutoField(primary_key=True, serialize=False)),
                ('room_no', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('allotment_startdate', models.DateField(blank=True, null=True)),
                ('allotment_enddate', models.DateField(blank=True, null=True)),
                ('priority_no', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
            ],
            options={
                'db_table': 'ncp_accomodation_approval',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NcpAccomodationCheck',
            fields=[
                ('ncp_chk_id', models.AutoField(primary_key=True, serialize=False)),
                ('no_room_allotted_sop', models.IntegerField(blank=True, null=True)),
                ('total_room_allotted', models.IntegerField(blank=True, null=True)),
                ('space_available_room', models.IntegerField(blank=True, null=True)),
                ('space_for_total_student', models.IntegerField(blank=True, null=True)),
                ('availability', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ncp_accomodation_check',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NcpDues',
            fields=[
                ('dues_id', models.AutoField(primary_key=True, serialize=False)),
                ('it_branch', models.BooleanField(blank=True, null=True)),
                ('ncpemployee_id', models.IntegerField(blank=True, null=True)),
                ('mehanical_workshop', models.BooleanField(blank=True, null=True)),
                ('finance_branch', models.BooleanField(blank=True, null=True)),
                ('security_branch', models.BooleanField(blank=True, null=True)),
                ('hr_branch', models.BooleanField(blank=True, null=True)),
                ('transport_section', models.BooleanField(blank=True, null=True)),
                ('telephone_exchange', models.BooleanField(blank=True, null=True)),
                ('store_branch', models.BooleanField(blank=True, null=True)),
                ('estate_branch', models.BooleanField(blank=True, null=True)),
                ('ncp_libaray', models.BooleanField(blank=True, null=True)),
                ('a_ai_branch', models.BooleanField(blank=True, db_column='A_AI_branch', null=True)),
            ],
            options={
                'db_table': 'ncp_dues',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NcpPublications',
            fields=[
                ('ncppublications_id', models.AutoField(primary_key=True, serialize=False)),
                ('no_papers_published', models.IntegerField(blank=True, null=True)),
                ('no_papers_accepted', models.IntegerField(blank=True, null=True)),
                ('no_papers_submitted', models.IntegerField(blank=True, null=True)),
                ('no_papers_presented', models.IntegerField(blank=True, null=True)),
                ('no_patents_submitted', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ncp_publications',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PublicationsList',
            fields=[
                ('publications_id', models.AutoField(primary_key=True, serialize=False)),
                ('publications_name', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('publications_document', models.BinaryField(blank=True, max_length='max', null=True)),
            ],
            options={
                'db_table': 'publications_list',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('std_cnic', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, primary_key=True, serialize=False)),
                ('std_name', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('std_email', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('std_phone_no', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('std_password', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('verification_code', models.IntegerField(blank=True, null=True)),
                ('verification_status', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
            ],
            options={
                'db_table': 'student',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentPictures',
            fields=[
                ('std_pic_id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='student_pictures/')),
            ],
            options={
                'db_table': 'student_pictures',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentRegistration',
            fields=[
                ('reg_form_id', models.AutoField(primary_key=True, serialize=False)),
                ('dob', models.DateField(blank=True, null=True)),
                ('highest_qualification', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=150, null=True)),
                ('academic_record', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', db_column='academic_Record', max_length=250, null=True)),
                ('present_status', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=250, null=True)),
                ('designation', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=100, null=True)),
                ('university_reg_no', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('present_university_name', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=100, null=True)),
                ('permanent_address', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=200, null=True)),
                ('mailing_address', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=200, null=True)),
                ('landline_no', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
            ],
            options={
                'db_table': 'student_registration',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TransportMemberProforma',
            fields=[
                ('transport_form_id', models.AutoField(primary_key=True, serialize=False)),
                ('transport_application_date', models.DateField(blank=True, null=True)),
                ('transport_req_start_date', models.DateField(blank=True, null=True)),
                ('transport_req_end_date', models.DateField(blank=True, null=True)),
                ('pick_drop_point', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('lab_contact_no', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('application_status', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
            ],
            options={
                'db_table': 'transport_member_proforma',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UniversitySupervisor',
            fields=[
                ('supervisor_id', models.AutoField(primary_key=True, serialize=False)),
                ('supervisor_name', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('supervisor_designation', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('supervisor_phone_no', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('supervisor_fax_no', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('supervisor_email', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
                ('supervisor_department', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=50, null=True)),
            ],
            options={
                'db_table': 'university_supervisor',
                'managed': False,
            },
        ),
    ]
