CREATE TABLE IF NOT EXISTS `django_migrations` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `app` VARCHAR(255) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `applied` DATETIME NOT NULL
);

INSERT INTO `django_migrations` VALUES
    (1,'contenttypes','0001_initial','2024-04-24 04:48:52.037292'),
    (2,'contenttypes','0002_remove_content_type_name','2024-04-24 04:48:52.116695'),
    (3,'auth','0001_initial','2024-04-24 04:48:52.366568'),
    (4,'auth','0002_alter_permission_name_max_length','2024-04-24 04:48:52.414855'),
    (5,'auth','0003_alter_user_email_max_length','2024-04-24 04:48:52.532854'),
    (6,'auth','0004_alter_user_username_opts','2024-04-24 04:48:52.578354'),
    (7,'auth','0005_alter_user_last_login_null','2024-04-24 04:48:52.631002'),
    (8,'auth','0006_require_contenttypes_0002','2024-04-24 04:48:52.680199'),
    (9,'auth','0007_alter_validators_add_error_messages','2024-04-24 04:48:52.753480'),
    (10,'auth','0008_alter_user_username_max_length','2024-04-24 04:48:52.811630'),
    (11,'auth','0009_alter_user_last_name_max_length','2024-04-24 04:48:52.895002'),
    (12,'auth','0010_alter_group_name_max_length','2024-04-24 04:48:52.946757'),
    (13,'auth','0011_update_proxy_permissions','2024-04-24 04:48:53.020848'),
    (14,'auth','0012_alter_user_first_name_max_length','2024-04-24 04:48:53.111701'),
    (15,'app','0001_initial','2024-04-24 04:48:53.440583'),
    (16,'admin','0001_initial','2024-04-24 04:48:53.666848'),
    (17,'admin','0002_logentry_remove_auto_add','2024-04-24 04:48:53.746859'),
    (18,'admin','0003_logentry_add_action_flag_choices','2024-04-24 04:48:53.885144'),
    (19,'sessions','0001_initial','2024-04-24 04:48:54.047916');

CREATE TABLE IF NOT EXISTS `django_content_type` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `app_label` VARCHAR(100) NOT NULL,
    `model` VARCHAR(100) NOT NULL
);

INSERT INTO `django_content_type` VALUES
    (1,'app','catalog'),
    (2,'app','centre'),
    (3,'app','cicle'),
    (4,'app','log'),
    (5,'app','tipusmaterial'),
    (6,'app','br'),
    (7,'app','cd'),
    (8,'app','dispositiu'),
    (9,'app','dvd'),
    (10,'app','llibre'),
    (11,'app','usuari'),
    (12,'app','elementcatalog'),
    (13,'app','exemplar'),
    (14,'app','imatgecatalog'),
    (15,'app','peticio'),
    (16,'app','prestec'),
    (17,'app','reserva'),
    (18,'admin','logentry'),
    (19,'auth','permission'),
    (20,'auth','group'),
    (21,'contenttypes','contenttype'),
    (22,'sessions','session');

CREATE TABLE IF NOT EXISTS `auth_permission` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `content_type_id` INT NOT NULL,
    `codename` VARCHAR(100) NOT NULL,
    `name` VARCHAR(255) NOT NULL
);

INSERT INTO `auth_permission` VALUES
    (1,1,'add_catalog','Can add catalog'),
    (2,1,'change_catalog','Can change catalog'),
    (3,1,'delete_catalog','Can delete catalog'),
    (4,1,'view_catalog','Can view catalog'),
    (5,2,'add_centre','Can add centre'),
    (6,2,'change_centre','Can change centre'),
    (7,2,'delete_centre','Can delete centre'),
    (8,2,'view_centre','Can view centre'),
    (9,3,'add_cicle','Can add cicle'),
    (10,3,'change_cicle','Can change cicle'),
    (11,3,'delete_cicle','Can delete cicle'),
    (12,3,'view_cicle','Can view cicle'),
    (13,4,'add_log','Can add log'),
    (14,4,'change_log','Can change log'),
    (15,4,'delete_log','Can delete log'),
    (16,4,'view_log','Can view log'),
    (17,5,'add_tipusmaterial','Can add tipus material'),
    (18,5,'change_tipusmaterial','Can change tipus material'),
    (19,5,'delete_tipusmaterial','Can delete tipus material'),
    (20,5,'view_tipusmaterial','Can view tipus material'),
    (21,6,'add_br','Can add br'),
    (22,6,'change_br','Can change br'),
    (23,6,'delete_br','Can delete br'),
    (24,6,'view_br','Can view br'),
    (25,7,'add_cd','Can add cd'),
    (26,7,'change_cd','Can change cd'),
    (27,7,'delete_cd','Can delete cd'),
    (28,7,'view_cd','Can view cd'),
    (29,8,'add_dispositiu','Can add dispositiu'),
    (30,8,'change_dispositiu','Can change dispositiu'),
    (31,8,'delete_dispositiu','Can delete dispositiu'),
    (32,8,'view_dispositiu','Can view dispositiu'),
    (33,9,'add_dvd','Can add dvd'),
    (34,9,'change_dvd','Can change dvd'),
    (35,9,'delete_dvd','Can delete dvd'),
    (36,9,'view_dvd','Can view dvd'),
    (37,10,'add_llibre','Can add llibre'),
    (38,10,'change_llibre','Can change llibre'),
    (39,10,'delete_llibre','Can delete llibre'),
    (40,10,'view_llibre','Can view llibre'),
    (41,11,'add_usuari','Can add usuari'),
    (42,11,'change_usuari','Can change usuari'),
    (43,11,'delete_usuari','Can delete usuari'),
    (44,11,'view_usuari','Can view usuari'),
    (45,12,'add_elementcatalog','Can add element catalog'),
    (46,12,'change_elementcatalog','Can change element catalog'),
    (47,12,'delete_elementcatalog','Can delete element catalog'),
    (48,12,'view_elementcatalog','Can view element catalog'),
    (49,13,'add_exemplar','Can add exemplar'),
    (50,13,'change_exemplar','Can change exemplar'),
    (51,13,'delete_exemplar','Can delete exemplar'),
    (52,13,'view_exemplar','Can view exemplar'),
    (53,14,'add_imatgecatalog','Can add imatge catalog'),
    (54,14,'change_imatgecatalog','Can change imatge catalog'),
    (55,14,'delete_imatgecatalog','Can delete imatge catalog'),
    (56,14,'view_imatgecatalog','Can view imatge catalog'),
    (57,15,'add_peticio','Can add peticio'),
    (58,15,'change_peticio','Can change peticio'),
    (59,15,'delete_peticio','Can delete peticio'),
    (60,15,'view_peticio','Can view peticio'),
    (61,16,'add_prestec','Can add prestec'),
    (62,16,'change_prestec','Can change prestec'),
    (63,16,'delete_prestec','Can delete prestec'),
    (64,16,'view_prestec','Can view prestec'),
    (65,17,'add_reserva','Can add reserva'),
    (66,17,'change_reserva','Can change reserva'),
    (67,17,'delete_reserva','Can delete reserva'),
    (68,17,'view_reserva','Can view reserva');

CREATE TABLE IF NOT EXISTS `auth_group` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `group_id` INT NOT NULL,
    `permission_id` INT NOT NULL,
    FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `auth_user` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `password` VARCHAR(128) NOT NULL,
    `last_login` DATETIME NULL,
    `is_superuser` BOOLEAN NOT NULL,
    `username` VARCHAR(150) NOT NULL UNIQUE,
    `first_name` VARCHAR(30) NOT NULL,
    `last_name` VARCHAR(150) NOT NULL,
    `email` VARCHAR(254) NOT NULL,
    `is_staff` BOOLEAN NOT NULL,
    `is_active` BOOLEAN NOT NULL,
    `date_joined` DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `group_id` INT NOT NULL,
    FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `permission_id` INT NOT NULL,
    FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `django_admin_log` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `action_time` DATETIME NOT NULL,
    `object_id` TEXT NULL,
    `object_repr` VARCHAR(200) NOT NULL,
    `action_flag` SMALLINT UNSIGNED NOT NULL,
    `change_message` TEXT NOT NULL,
    `content_type_id` INT NULL,
    `user_id` INT NOT NULL,
    FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE SET NULL,
    FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `django_session` (
    `session_key` VARCHAR(40) NOT NULL PRIMARY KEY,
    `session_data` TEXT NOT NULL,
    `expire_date` DATETIME NOT NULL
);
