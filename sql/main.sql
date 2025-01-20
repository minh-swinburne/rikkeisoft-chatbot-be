select * from users;
select * from chats;
select * from messages;
select * from documents;
-- select * from sso_providers;
select * from sso;
select * from roles;

SELECT CURRENT_TIMESTAMP;

ALTER TABLE `users`
	DROP COLUMN `username_last_changed`,
	ADD COLUMN `username_last_changed` datetime;

CREATE TABLE `documents` (
  `id` char(36) NOT NULL PRIMARY KEY,
  `filename` varchar(255) NOT NULL,
  `file_type` varchar(50) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text,
  `categories` varchar(255) not null,
  `creator` char(36) not null,
  `created_date` date,
  `restricted` bool not null,
  `uploader` char(36) not null,
  `uploaded_time` datetime default current_timestamp,
  foreign key (`creator`) references `users`(`id`),
  foreign key (`uploader`) references `users`(`id`)
);

DROP TABLE IF EXISTS `sso_providers`;
CREATE TABLE `sso_providers` (
	`id` int primary key,
    `name` varchar(50) unique
);

insert into `sso_providers` values (1, 'google'), (2, 'microsoft');

DROP TABLE IF EXISTS `sso`;
create table `sso` (
	`user_id` char(36) not null,
    `provider` enum('google', 'microsoft') not null,
    `sub` varchar(100) not null,
    primary key (`user_id`, `provider`),
    foreign key (`user_id`) references `users`(`id`)
);

INSERT INTO `sso` VALUES ('1642be2a-e3a9-4679-87eb-1365f9f470d0', 'google', '107360694239114519362');
INSERT INTO `sso` VALUES ('ddfa1b08-e3c0-4cca-84d7-ac70e60f856d', 'microsoft', 'AAAAAAAAAAAAAAAAAAAAAAGWQBsfLK99T6YSqJXyY4s');

CREATE TABLE `roles` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255)
);

INSERT INTO `roles` (`name`, `description`) VALUES ('system_admin', ''), ('admin', ''), ('employee', '');

CREATE TABLE user_roles (
    user_id VARCHAR(36) NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

INSERT INTO `user_roles` VALUES ('c24d9619-848d-4af6-87c8-718444421762', 1), ('c24d9619-848d-4af6-87c8-718444421762', 2), ('c24d9619-848d-4af6-87c8-718444421762', 3), ('1642be2a-e3a9-4679-87eb-1365f9f470d0', 3), ('86ce47d5-0bf4-47c4-adb4-2be068e73580', 2), ('86ce47d5-0bf4-47c4-adb4-2be068e73580', 3), ('ddfa1b08-e3c0-4cca-84d7-ac70e60f856d', 3);

CREATE TABLE `categories` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255)
);

INSERT INTO categories (name, description) VALUES
    ('Guidance', 'Documents providing guidance'),
    ('Policies', 'Policy-related documents'),
    ('Reports', 'Reports and summaries'),
    ('Procedures', 'Operational procedures'),
    ('Training Materials', 'Documents for training purposes'),
    ('Technical Documentation', 'Technical reference documents');

DROP TABLE IF EXISTS document_categories;
CREATE TABLE document_categories (
    document_id VARCHAR(36) NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (document_id, category_id),
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

INSERT INTO document_categories (document_id, category_id) VALUES
    ('075b414e-b346-43ec-8c60-8f3d7e1c4772', 1),
    ('075b414e-b346-43ec-8c60-8f3d7e1c4772', 5),
    ('20fec429-7b9d-47e5-bc68-4adcdddeb72c', 5),
    ('20fec429-7b9d-47e5-bc68-4adcdddeb72c', 6),
    ('20fec429-7b9d-47e5-bc68-4adcdddeb72c', 3),
    ('20fec429-7b9d-47e5-bc68-4adcdddeb72c', 4),
    ('44a694c1-9aae-4801-ada4-10cdbd4f712b', 5),
    ('cf4593be-0ee6-4257-a9a5-79c27aa9ac61', 1),
    ('cf4593be-0ee6-4257-a9a5-79c27aa9ac61', 5);