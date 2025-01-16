select * from users;
select * from chats;
select * from messages;
select * from documents;
select * from sso_providers;
select * from sso_accounts;

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

DROP TABLE IF EXISTS `sso_accounts`;
create table `sso_accounts` (
	`user_id` char(36) not null,
    `provider_id` int not null,
    `sub` varchar(100) not null,
    primary key (`user_id`, `provider_id`),
    foreign key (`user_id`) references `users`(`id`),
    foreign key (`provider_id`) references `sso_providers`(`id`)
);

INSERT INTO `sso_accounts` VALUES ('1642be2a-e3a9-4679-87eb-1365f9f470d0', 1, '107360694239114519362');
INSERT INTO `sso_accounts` VALUES ('ddfa1b08-e3c0-4cca-84d7-ac70e60f856d', 2, 'AAAAAAAAAAAAAAAAAAAAAAGWQBsfLK99T6YSqJXyY4s');