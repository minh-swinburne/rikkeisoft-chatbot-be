-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: rikkeigpt-db.cb4mi4quoniq.ap-southeast-2.rds.amazonaws.com
-- Generation Time: Feb 09, 2025 at 07:51 AM
-- Server version: 8.0.40
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rikkeigpt`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `description`) VALUES
(1, 'Guidance', 'Documents providing guidance'),
(2, 'Policies', 'Policy-related documents'),
(3, 'Reports', 'Reports and summaries'),
(4, 'Procedures', 'Operational procedures'),
(5, 'Training Materials', 'Documents for training purposes'),
(6, 'Technical Documentation', 'Technical reference documents');

-- --------------------------------------------------------

--
-- Table structure for table `chats`
--

CREATE TABLE `chats` (
  `id` char(36) NOT NULL,
  `user_id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `last_access` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `chats`
--

INSERT INTO `chats` (`id`, `user_id`, `name`, `last_access`) VALUES
('01945c9c-50cf-7c99-91b1-4efefc51f08b', '86ce47d5-0bf4-47c4-adb4-2be068e73580', 'Specialized Chat: Conversations Within Conundrums', '2025-01-13 05:51:10'),
('01945c9d-06cb-7221-85fb-1c210e064d80', '86ce47d5-0bf4-47c4-adb4-2be068e73580', '\"PulseForge\"', '2025-01-13 05:48:32'),
('01945c9d-aab6-770d-9fd1-d2e6842c5134', '86ce47d5-0bf4-47c4-adb4-2be068e73580', 'Tool Talk: A Guide to Efficiency in Conversations', '2025-01-13 05:51:51'),
('01945c9e-4aef-7a44-bd3e-c52d0c4b12f0', '86ce47d5-0bf4-47c4-adb4-2be068e73580', 'After analyzing the chat history, I generated a unique name that is relevant to the', '2025-01-13 05:47:38'),
('01945c9f-2951-7f07-a96f-8ffa5096e919', '86ce47d5-0bf4-47c4-adb4-2be068e73580', 'New Chat', '2025-01-13 05:25:22'),
('01945caf-f562-7a5d-a293-e17156e016ab', '86ce47d5-0bf4-47c4-adb4-2be068e73580', 'Markdown file with YAML', '2025-01-13 05:51:39'),
('01945cb2-21ab-7006-835d-fdca18a39ec6', '86ce47d5-0bf4-47c4-adb4-2be068e73580', 'It seems like you started to type something, but it got cut off. Could', '2025-01-13 05:46:16'),
('01945cbb-3f6d-7fab-a0b1-336d2c32fa65', '1642be2a-e3a9-4679-87eb-1365f9f470d0', 'Language Liaison Between Human and AI: Resource and Assistance for Solving Life', '2025-01-13 05:57:10'),
('01945f21-f105-7f4d-b69a-fff71fdbb61d', 'c24d9619-848d-4af6-87c8-718444421762', 'Understanding at the Interface of Technology and', '2025-01-13 17:20:32'),
('01945f53-d543-7ced-bbcb-96cdb1c90c9c', 'c24d9619-848d-4af6-87c8-718444421762', 'Minhwave', '2025-01-14 13:36:41'),
('0194da67-4e79-76c4-a632-8ff60b9fcf4a', 'c24d9619-848d-4af6-87c8-718444421762', 'Markdown Cell Formatting', '2025-02-06 15:50:59'),
('0194da69-8b7c-7081-9283-0dc94d907fc0', 'c24d9619-848d-4af6-87c8-718444421762', 'Markdown Table Cell Multiline Text', '2025-02-06 15:39:04'),
('0194da81-e053-7c2e-8d5d-555b3892467b', 'c24d9619-848d-4af6-87c8-718444421762', 'Unit Outline Summary', '2025-02-06 16:05:43'),
('0194da84-2162-7b61-80e8-756bb35ed772', 'c24d9619-848d-4af6-87c8-718444421762', 'Project Management Mastery', '2025-02-06 16:08:07'),
('0194da8b-5efe-7b49-9893-a52fc57ff89d', 'c24d9619-848d-4af6-87c8-718444421762', 'SmartHealth Week 2 Review', '2025-02-09 07:30:11'),
('0194da93-b057-7c9e-9e0b-137d7c305d96', 'f7e0386e-8e56-464b-82ef-19747f6a9bae', ' COS40005 Context', '2025-02-06 16:25:04'),
('67763113-27cc-800f-a79c-3663c53de570', 'c24d9619-848d-4af6-87c8-718444421762', 'Birthday Gift for Father', '2019-01-20 00:01:00'),
('6776cdc6-cfa0-800f-bf3f-e3dedb47431f', 'c24d9619-848d-4af6-87c8-718444421762', 'New Chat', '2025-01-13 15:34:02'),
('a1e8d106-6589-4e45-97c6-f623d5824a49', 'c24d9619-848d-4af6-87c8-718444421762', 'Expert Marketing Strategies', '2025-01-13 05:54:46'),
('f0033470-99d2-4aa1-af8a-79b9e29e9dbf', 'c24d9619-848d-4af6-87c8-718444421762', 'The Crash 27', '2025-01-13 14:04:42'),
('f0cd3940-44ab-4f48-bcc9-d5f2dd3d833d', 'c24d9619-848d-4af6-87c8-718444421762', 'New Chat', '2025-01-10 00:01:22');

-- --------------------------------------------------------

--
-- Table structure for table `documents`
--

CREATE TABLE `documents` (
  `id` char(36) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_type` enum('pdf','docx','xlsx','html') NOT NULL,
  `link_url` text,
  `title` varchar(255) NOT NULL,
  `description` text,
  `creator` char(36) NOT NULL,
  `created_date` date DEFAULT NULL,
  `restricted` tinyint DEFAULT '0',
  `uploader` char(36) NOT NULL,
  `uploaded_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_modified` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `documents`
--

INSERT INTO `documents` (`id`, `file_name`, `file_type`, `link_url`, `title`, `description`, `creator`, `created_date`, `restricted`, `uploader`, `uploaded_time`, `last_modified`) VALUES
('835babdf-2b81-413e-aa71-61483b4cb3a5', 'progression-2023-tables.xlsx', 'xlsx', NULL, 'progression-2023-tables', 'progression-2023-tables', 'c24d9619-848d-4af6-87c8-718444421762', '2025-02-06', 0, 'c24d9619-848d-4af6-87c8-718444421762', '2025-02-06 09:39:54', '2025-02-06 09:39:54'),
('88062a21-84f2-4015-9f5c-200fcdda6c33', 'COS40005 Sprint 1 Project Specification.docx', 'docx', NULL, 'COS40005 Sprint 1 Project Specification', 'COS40005 Sprint 1', 'c24d9619-848d-4af6-87c8-718444421762', '2025-02-06', 1, 'c24d9619-848d-4af6-87c8-718444421762', '2025-02-06 09:39:10', '2025-02-06 09:39:10'),
('9465c7e0-8560-4c84-9d78-2b970c75db84', 'Markdown multiline code blocks in tables when rows have to be specified with one-liners - Stack Overflow.html', 'html', 'https://stackoverflow.com/questions/24190085/markdown-multiline-code-blocks-in-tables-when-rows-have-to-be-specified-with-one', 'Markdown multiline code blocks in tables when rows have to be specified with one-liners', '', 'f7e0386e-8e56-464b-82ef-19747f6a9bae', '2025-02-06', 0, 'c24d9619-848d-4af6-87c8-718444421762', '2025-02-06 15:37:45', '2025-02-06 15:37:45'),
('dd43369c-575c-425a-aaa9-3ada0486cfa3', 'COS40005 Worklog - Week 2.pdf', 'pdf', NULL, 'COS40005 Worklog - Week 2', '', '1642be2a-e3a9-4679-87eb-1365f9f470d0', '2025-01-22', 1, 'c24d9619-848d-4af6-87c8-718444421762', '2025-02-06 16:13:48', '2025-02-06 16:13:48'),
('f086ae23-dd83-4611-9ca0-04d75c9a9fb3', 'HTMLImageElement srcset property - Web APIs  MDN.html', 'html', 'https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/srcset#examples', 'HTMLImageElement: srcset property', '', '86ce47d5-0bf4-47c4-adb4-2be068e73580', '2025-02-06', 0, 'c24d9619-848d-4af6-87c8-718444421762', '2025-02-07 00:28:37', '2025-02-07 00:28:37');

-- --------------------------------------------------------

--
-- Table structure for table `document_categories`
--

CREATE TABLE `document_categories` (
  `document_id` char(36) NOT NULL,
  `category_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `document_categories`
--

INSERT INTO `document_categories` (`document_id`, `category_id`) VALUES
('835babdf-2b81-413e-aa71-61483b4cb3a5', 1),
('9465c7e0-8560-4c84-9d78-2b970c75db84', 1),
('f086ae23-dd83-4611-9ca0-04d75c9a9fb3', 1),
('88062a21-84f2-4015-9f5c-200fcdda6c33', 3),
('dd43369c-575c-425a-aaa9-3ada0486cfa3', 3),
('dd43369c-575c-425a-aaa9-3ada0486cfa3', 4),
('9465c7e0-8560-4c84-9d78-2b970c75db84', 6),
('f086ae23-dd83-4611-9ca0-04d75c9a9fb3', 6);

-- --------------------------------------------------------

--
-- Table structure for table `document_status`
--

CREATE TABLE `document_status` (
  `document_id` char(36) NOT NULL,
  `uploaded` enum('pending','processing','complete','error') DEFAULT 'pending',
  `embedded` enum('pending','processing','complete','error') DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `document_status`
--

INSERT INTO `document_status` (`document_id`, `uploaded`, `embedded`) VALUES
('835babdf-2b81-413e-aa71-61483b4cb3a5', 'complete', 'complete'),
('88062a21-84f2-4015-9f5c-200fcdda6c33', 'complete', 'complete'),
('9465c7e0-8560-4c84-9d78-2b970c75db84', 'complete', 'complete'),
('dd43369c-575c-425a-aaa9-3ada0486cfa3', 'complete', 'complete'),
('f086ae23-dd83-4611-9ca0-04d75c9a9fb3', 'complete', 'complete');

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` char(36) NOT NULL,
  `chat_id` char(36) NOT NULL,
  `time` datetime DEFAULT CURRENT_TIMESTAMP,
  `role` varchar(50) NOT NULL,
  `content` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`id`, `chat_id`, `time`, `role`, `content`) VALUES
('01945c88-ed48-79cf-81c1-f9384404b28f', '67763113-27cc-800f-a79c-3663c53de570', '2019-01-20 00:00:00', 'user', 'What gifts should I give my father on his birthday?'),
('01945c89-0069-7cb1-9ce8-ea415b2d2a30', '67763113-27cc-800f-a79c-3663c53de570', '2019-01-20 00:00:04', 'assistant', 'The ideal gift for your father\'s birthday depends on his interests, hobbies, and preferences. Here are some popular gift ideas:\n\n1. **Personalized items**: Engraved watch, monogrammed wallet, or a photo album with fond memories.\n2. **Tech gadgets**: Smartwatch, wireless headphones, or a high-tech smartphone accessory.\n3. **Experiences**: Tickets to a sporting event or a concert, a weekend getaway, or a fun activity he\'s always wanted to try (e.g., golfing, fishing, or cooking class).\n4. **Luxury grooming**: High-quality shaving kit, luxurious fragrances, or a rejuvenating spa day.\n5. **Hobby-related gifts**: If your father enjoys a particular hobby, consider gifting him something related, such as:\n	* For the outdoorsy type: camping gear, hiking equipment, or a new bike.\n	* For the foodie: cookbook, wine and cheese basket, or a kitchen appliance.\n	* For the sports enthusiast: autographed jersey, sports memorabilia, or a new piece of equipment.\n6. **Practical items**: A high-quality wallet, a leather bag, or a functional tool for his workshop or garage.\n7. **Subscription services**: Sign him up for a streaming platform, a monthly wine club, or a magazine subscription that aligns with his interests.\n\nRemember, the most important aspect of a gift is the thought and love behind it. Choose something that shows you care and pay attention to his interests and preferences.\n\nSources:\n- Various online gift guides and reviews (e.g., The Spruce, Wirecutter, and Esquire).\n- Personal experience and common gift-giving practices.'),
('01945c89-1104-7028-a666-e3d6cd96d6cc', '6776cdc6-cfa0-800f-bf3f-e3dedb47431f', '2025-01-10 00:04:07', 'user', 'test'),
('01945c8a-1cd6-7b7e-baf0-2af66a51304c', '6776cdc6-cfa0-800f-bf3f-e3dedb47431f', '2025-01-10 00:04:07', 'assistant', 'It seems like you\'re testing the system. Is there something specific you\'d like to know or discuss? I\'m here to help with any questions you might have.'),
('01945c8c-ddd0-763c-9623-82e099fc4592', '67763113-27cc-800f-a79c-3663c53de570', '2025-01-13 05:05:23', 'user', '[What are some gift ideas for a father\'s birthday in a retirement home setting?]'),
('01945c8c-e7dd-7149-acb2-2f9234e352eb', '67763113-27cc-800f-a79c-3663c53de570', '2025-01-13 05:05:26', 'assistant', 'When considering gift ideas for a father\'s birthday in a retirement home setting, it\'s essential to prioritize items that promote comfort, entertainment, and social interaction. Here are some thoughtful gift ideas:\n\n1. **Personalized comfort items**:\n	* Soft, cozy blankets or throws with his name or initials.\n	* A favorite pillow or plush toy for companionship.\n2. **Entertainment and leisure**:\n	* A tablet or e-reader pre-loaded with his favorite books, music, or games.\n	* A puzzle book, crossword, or deck of cards for mental stimulation.\n	* A DVD player or streaming device with his favorite movies or TV shows.\n3. **Social interaction**:\n	* A gift certificate for a special outing or activity with family or friends, such as a scenic drive or a visit to a local attraction.\n	* A board game or card game that encourages socializing with other residents.\n4. **Practical items**:\n	* A comfortable, easy-to-use phone or phone accessory, such as a simple phone with large buttons.\n	* A personalized calendar or planner to stay organized and connected with loved ones.\n	* A set of nice notecards or stationery for writing letters or sending greetings.\n5. **Sensory delights**:\n	* A favorite snack or dessert, such as chocolates or fresh fruit.\n	* A scented candle, essential oil diffuser, or a bouquet of fresh flowers for a pleasant atmosphere.\n6. **Memories and nostalgia**:\n	* A personalized photo album or frame with pictures of loved ones and fond memories.\n	* A customized playlist of his favorite music from throughout the years.\n7. **Care and wellness**:\n	* A cozy robe or comfortable slippers for everyday wear.\n	* A gift certificate for a massage, manicure, or other spa treatment to promote relaxation and well-being.\n\nRemember to consider your father\'s specific needs, interests, and abilities when choosing a gift. It\'s also a good idea to consult with the retirement home staff to ensure the gift is suitable and safe for the environment.\n\nSources:\n- American Association of Retired Persons (AARP) gift guides.\n- National Institute on Aging (NIA) recommendations for older adults.\n- Personal experience and feedback from caregivers and residents in retirement home settings.'),
('01945c9f-9e7d-78a2-904c-99a9164a4c3f', '01945c9f-2951-7f07-a96f-8ffa5096e919', '2025-01-13 05:25:52', 'user', 'Which document format is suitable for referencing multiple projects in a single document?'),
('01945c9f-a2fa-7710-a41a-3f551ca2983f', '01945c9f-2951-7f07-a96f-8ffa5096e919', '2025-01-13 05:25:53', 'assistant', 'A Portable Document Format (PDF) or a Microsoft Word document (.docx) can be suitable for referencing multiple projects in a single document. However, a more structured approach would be to use a document format like a Microsoft Excel spreadsheet (.xlsx) or a Markdown file (.md) with links and cross-references.\n\nBut if you\'re looking for a more formal and standardized document format, you might consider using:\n\n1. **Microsoft Project file** (.mpp): This format is specifically designed for project management and can handle multiple projects.\n2. **Excel workbook** (.xlsx): This format is versatile and can be used to create a dashboard or a report that references multiple projects.\n3. **Markdown file with YAML front matter** (.md): This format is lightweight and can be used to create a document that references multiple projects, with metadata stored in the YAML front matter.\n\nUltimately, the choice of document format depends on your specific needs, the complexity of your projects, and the tools you\'re already using.\n\nSources:\n- Microsoft Project documentation\n- Excel documentation\n- Markdown documentation'),
('01945cb0-706c-7226-8593-d93753c68680', '01945caf-f562-7a5d-a293-e17156e016ab', '2025-01-13 05:44:15', 'user', 'Can a Markdown file with YAML front matter be used for creating a company-wide project portfolio?'),
('01945cb0-7605-7483-b5e4-5810cb63f5e3', '01945caf-f562-7a5d-a293-e17156e016ab', '2025-01-13 05:44:16', 'assistant', '**Yes**, a Markdown file with YAML front matter can be used for creating a company-wide project portfolio. \n\nHere\'s why:\n* Markdown allows for easy formatting and readability, making it simple to create and update project descriptions.\n* YAML front matter enables the addition of metadata, such as project titles, dates, and tags, which can be used for organization and filtering.\n* This combination allows for a flexible and scalable way to manage project information, making it suitable for a company-wide project portfolio.\n\nTo implement this, you can use static site generators like Jekyll or Hugo, which support Markdown and YAML front matter, to create a portfolio website. Additionally, tools like GitHub Pages or GitLab Pages can be used to host and manage the portfolio. \n\nSources:\n* [Markdown documentation](https://www.markdownguide.org/)\n* [YAML documentation](https://yaml.org/spec/1.2/spec.html)\n* [Jekyll documentation](https://jekyllrb.com/docs/)\n* [Hugo documentation](https://gohugo.io/documentation/)'),
('01945cb2-43d1-71cd-9469-d0317b44d301', '01945cb2-21ab-7006-835d-fdca18a39ec6', '2025-01-13 05:46:14', 'user', 'How can I verify the author\'s information?'),
('01945cb2-4862-7ba1-91ba-2465b8a9b8b0', '01945cb2-21ab-7006-835d-fdca18a39ec6', '2025-01-13 05:46:15', 'assistant', 'To verify an author\'s information, you can try the following steps:\n\n1. **Check the book or publication**: Look for the author\'s biography or about the author section in the book or publication.\n2. **Official website or social media**: Visit the author\'s official website or social media profiles to see if they have provided information about themselves.\n3. **Literary directories or databases**: Search online literary directories or databases, such as Goodreads, Wikipedia, or Publishers Weekly, which may have information about the author.\n4. **Contact the publisher**: Reach out to the publisher of the book or publication and ask if they can provide verification of the author\'s information.\n5. **Check with professional organizations**: If the author is a member of a professional organization, such as a writers\' association, you can contact the organization to verify the author\'s membership and credentials.\n\nBy taking these steps, you should be able to verify the author\'s information. If you\'re unable to find the information you\'re looking for, you can also try contacting the author directly or seeking help from a librarian or research assistant.'),
('01945cb3-8349-7d87-9421-cdf42aadbd0f', '01945c9e-4aef-7a44-bd3e-c52d0c4b12f0', '2025-01-13 05:47:36', 'user', 'What features does this chatbot have?'),
('01945cb3-88d3-7110-92d3-f5afc6921db6', '01945c9e-4aef-7a44-bd3e-c52d0c4b12f0', '2025-01-13 05:47:37', 'assistant', 'I have several features that enable me to provide helpful and informative responses. Some of my key features include:\n\n1. **Knowledge Base**: I have been trained on a vast amount of text data, which allows me to provide answers to a wide range of questions and topics.\n2. **Natural Language Processing (NLP)**: I can understand and process human language, allowing users to interact with me in a conversational manner.\n3. **Contextual Understanding**: I can understand the context of a conversation and respond accordingly.\n4. **Question Answering**: I can provide direct answers to user questions, citing relevant sources and documents when available.\n5. **Concise Responses**: I strive to provide concise and to-the-point responses, avoiding unnecessary information.\n6. **Adaptability**: I can adapt to different topics and areas of discussion, providing relevant information and insights.\n7. **Limited Domain Knowledge**: My knowledge is limited to my training data, and I may not always have the most up-to-date or accurate information on very specific or niche topics.\n\nPlease note that my features are based on my training data, and I may not always be able to provide perfect responses. If I\'m unsure or don\'t know the answer to a question, I will let the user know.'),
('01945cb4-54df-7d49-b1cb-8a530c1d0b7f', '01945c9d-06cb-7221-85fb-1c210e064d80', '2025-01-13 05:48:30', 'user', 'What are the main differences between the \"Initial Proposal\" and \"Full Plan\"??'),
('01945cb4-5ae2-7e36-80ae-38f5af838791', '01945c9d-06cb-7221-85fb-1c210e064d80', '2025-01-13 05:48:31', 'assistant', 'The main differences between an \"Initial Proposal\" and a \"Full Plan\" typically include:\n\n1. **Level of detail**: An Initial Proposal provides a brief overview of the project, including its objectives, scope, and estimated costs. A Full Plan, on the other hand, provides a comprehensive and detailed outline of the project, including timelines, budgets, and resource allocation.\n2. **Scope and complexity**: An Initial Proposal usually outlines the overall scope and goals of the project, while a Full Plan breaks down the project into smaller, manageable tasks and provides a detailed analysis of the resources required to complete each task.\n3. **Stakeholder engagement**: An Initial Proposal is often used to gauge interest and secure funding or support for a project, while a Full Plan is typically used to guide the project team and stakeholders throughout the project lifecycle.\n4. **Timeline and milestones**: A Full Plan includes a detailed project schedule, including key milestones and deadlines, whereas an Initial Proposal may only provide a high-level timeline.\n5. **Budget and resource allocation**: A Full Plan provides a detailed breakdown of the project budget and resource allocation, including personnel, equipment, and materials, whereas an Initial Proposal may only provide an estimated total cost.\n\nIn general, an Initial Proposal is used to initiate a project or secure funding, while a Full Plan is used to guide the project team and stakeholders throughout the project lifecycle.\n\nSources:\n- Project Management Institute (PMI)\n- Agile Methodologies\n- Business Planning and Development resources\n\nPlease note that the specific differences between an Initial Proposal and a Full Plan may vary depending on the context, industry, or organization. If you have any further questions or would like more information, feel free to ask.'),
('01945cb6-c0b9-731e-a1de-835863838793', '01945c9c-50cf-7c99-91b1-4efefc51f08b', '2025-01-13 05:51:08', 'user', 'Can you mention any specific terms related to the topic of the conversation to identify areas of specialization?'),
('01945cb6-c469-7ea8-9673-b60b77bdf052', '01945c9c-50cf-7c99-91b1-4efefc51f08b', '2025-01-13 05:51:09', 'assistant', 'Since we haven\'t started a conversation yet, I don\'t have any specific terms to mention. However, I can suggest some general areas of specialization that might be relevant to a conversation, such as:\n\n1. **Artificial Intelligence (AI)**: machine learning, natural language processing, computer vision\n2. **Data Science**: data analysis, statistics, data visualization\n3. **Healthcare**: medical research, clinical trials, healthcare technology\n4. **Environmental Science**: climate change, sustainability, conservation biology\n5. **Computer Science**: software engineering, algorithms, cybersecurity\n\nPlease feel free to start a conversation, and I\'ll do my best to identify specific terms and areas of specialization relevant to the topic.'),
('01945cb7-61bf-7643-a7ea-331ffef577ab', '01945c9d-aab6-770d-9fd1-d2e6842c5134', '2025-01-13 05:51:50', 'user', 'How can I use this chat tool more effectively?'),
('01945cb7-650e-7e2a-927e-91cc597aed1b', '01945c9d-aab6-770d-9fd1-d2e6842c5134', '2025-01-13 05:51:50', 'assistant', 'To use this chat tool more effectively, follow these tips:\n\n1. **Be specific**: Clearly state your question or topic to get a precise answer.\n2. **Provide context**: Share relevant information about your question to help me understand your needs.\n3. **Ask one question at a time**: This allows me to focus on a single topic and provide a detailed response.\n4. **Use simple language**: Avoid using jargon or complex terminology unless necessary for your topic.\n5. **Check my capabilities**: I can provide information on a wide range of topics, but if I\'m unsure or don\'t know the answer, I\'ll let you know.\n\nBy following these guidelines, you\'ll be able to get the most out of our conversation and find the information you need efficiently.'),
('01945cba-0a27-70e1-ba0f-5555b5c85545', 'a1e8d106-6589-4e45-97c6-f623d5824a49', '2025-01-13 05:54:44', 'user', 'What are the most significant advantages of hiring an agency versus doing it in-house?'),
('01945cba-10cf-7dd7-b043-d663feb05a23', 'a1e8d106-6589-4e45-97c6-f623d5824a49', '2025-01-13 05:54:45', 'assistant', 'The most significant advantages of hiring an agency versus doing it in-house are:\n\n1. **Expertise and Specialization**: Agencies have specialized teams with extensive experience and knowledge in specific areas, such as marketing, advertising, or IT.\n2. **Cost Savings**: Hiring an agency can be more cost-effective than building and maintaining an in-house team, as agencies often have existing infrastructure and resources.\n3. **Flexibility and Scalability**: Agencies can quickly adapt to changing project requirements and scale up or down as needed, without the need for long-term commitments.\n4. **Access to Latest Technologies and Trends**: Agencies are often at the forefront of the latest technologies, tools, and trends, which can be beneficial for businesses that want to stay competitive.\n5. **Objectivity and Fresh Perspective**: Agencies can bring an objective and fresh perspective to a project, which can be beneficial for businesses that want to try new approaches or solutions.\n6. **Reduced Risk**: By outsourcing to an agency, businesses can transfer some of the risk associated with a project, such as timelines, budgets, and quality of work.\n7. **Faster Time-to-Market**: Agencies can often deliver projects faster than in-house teams, as they have existing processes and workflows in place.\n\nOverall, hiring an agency can be a strategic decision that allows businesses to tap into specialized expertise, reduce costs, and increase efficiency, while also mitigating risk and improving overall project outcomes.'),
('01945cbb-909b-73e9-ad63-e020af067a1e', '01945cbb-3f6d-7fab-a0b1-336d2c32fa65', '2025-01-13 05:56:24', 'user', 'How can you assist me?'),
('01945cbb-955c-7e86-b694-0e342902265d', '01945cbb-3f6d-7fab-a0b1-336d2c32fa65', '2025-01-13 05:56:25', 'assistant', 'I can assist you by providing information, answering questions, and helping with tasks such as:\n\n1. **Answering questions**: I can process natural language queries and provide relevant answers, covering a wide range of topics.\n2. **Providing definitions**: If you\'re unsure about the meaning of a word or phrase, I can define it for you.\n3. **Offering suggestions**: If you\'re looking for ideas or solutions to a problem, I can provide suggestions and guidance.\n4. **Generating text**: I can create text based on a prompt or topic, and can even help with writing tasks such as proofreading and editing.\n5. **Translation**: I can translate text from one language to another, including popular languages such as Spanish, French, German, Chinese, and many more.\n6. **Summarization**: If you have a large amount of text and want a concise summary, I can help with that.\n7. **Conversation**: I can engage in natural-sounding conversations, using context and understanding to respond to questions and statements.\n\nPlease let me know how I can assist you today. What\'s on your mind?'),
('01945cbc-40bd-7b7f-ba14-aa43fb2e442d', '01945cbb-3f6d-7fab-a0b1-336d2c32fa65', '2025-01-13 05:57:09', 'user', 'What are some basic tips for improving my writing skills?'),
('01945cbc-46ad-7e70-8f3f-c75ec243353f', '01945cbb-3f6d-7fab-a0b1-336d2c32fa65', '2025-01-13 05:57:10', 'assistant', 'Here are some basic tips to improve your writing skills:\n\n1. **Read widely**: Reading exposes you to different writing styles, genres, and techniques, which can help you develop your own writing voice.\n2. **Practice regularly**: Writing regularly helps to develop your writing muscle and improve your skills over time.\n3. **Plan and outline**: Before starting to write, create an outline to organize your thoughts and structure your writing.\n4. **Use clear and concise language**: Avoid using jargon and complex sentences that can confuse your readers.\n5. **Show, don\'t tell**: Instead of telling your readers what\'s happening, show them through descriptive language and sensory details.\n6. **Revise and edit**: Review your writing carefully to ensure it\'s free of errors and flows well.\n7. **Get feedback**: Share your writing with others and ask for feedback to help you identify areas for improvement.\n8. **Use active voice**: Using active voice makes your writing more engaging and easier to read.\n9. **Vary sentence structure**: Mixing up short and long sentences can create a more dynamic rhythm in your writing.\n10. **Learn grammar and punctuation rules**: Understanding the basics of grammar and punctuation is essential for effective writing.\n\nAdditionally, consider the following:\n\n* **Use a writing prompt** to get started\n* **Set writing goals** and deadlines to stay motivated\n* **Join a writing community** to connect with other writers and get support\n* **Take online courses or writing workshops** to learn new skills and techniques\n\nRemember, improving your writing skills takes time and practice. Be patient, persistent, and always keep learning.'),
('01945e79-8011-79f8-ac64-306dd3b8349b', 'f0033470-99d2-4aa1-af8a-79b9e29e9dbf', '2025-01-13 14:03:29', 'user', 'What triggered the stock market crash of 1929?'),
('01945e79-8741-7ab5-8bc8-69d0bd21b41f', 'f0033470-99d2-4aa1-af8a-79b9e29e9dbf', '2025-01-13 14:03:30', 'assistant', 'The stock market crash of 1929, also known as Black Tuesday, was triggered by a combination of factors. Some of the key events and conditions that contributed to the crash include:\n\n1. **Overproduction and underconsumption**: In the 1920s, there was a surge in industrial production, but many Americans were unable to afford the goods being produced, leading to a mismatch between supply and demand.\n2. **Speculation and margin buying**: Many investors bought stocks on margin (using borrowed money), hoping to make a quick profit. This created a fragile market that was vulnerable to sudden changes.\n3. **Weakening economy**: The economy was already showing signs of weakness in 1929, with declining industrial production, rising unemployment, and a slowdown in construction.\n4. **Credit crisis**: Many investors had bought stocks on margin, and when the market began to decline, they were unable to pay back their loans, leading to a credit crisis.\n5. **Banking system weaknesses**: The banking system at the time was fragile, and many banks had invested heavily in the stock market. When the market crashed, these banks found themselves with large losses, leading to widespread bank failures.\n\nThe immediate trigger for the crash was a **sharp decline in stock prices** on Thursday, October 24, 1929 (Black Thursday), which led to a wave of panic selling on Friday, October 25, and Monday, October 28. On Tuesday, October 29 (Black Tuesday), stock prices plummeted, with some stocks losing up to 50% of their value in a single day.\n\nSources:\n* \"A History of the American People\" by Paul Johnson\n* \"The Great Crash, 1929\" by John Kenneth Galbraith\n* \"The Stock Market Crash of 1929\" by the Federal Reserve History website.'),
('01945e7a-2afd-7b26-bd6e-5e2dc00cdf7e', 'f0033470-99d2-4aa1-af8a-79b9e29e9dbf', '2025-01-13 14:04:12', 'user', 'What is my birthday?'),
('01945e7a-2e0f-7db0-b119-76d4cb0e493b', 'f0033470-99d2-4aa1-af8a-79b9e29e9dbf', '2025-01-13 14:04:13', 'assistant', 'I don\'t have any information about your birthday. I\'m a text-based AI assistant and do not have access to personal data or user profiles. If you\'d like to share your birthday with me, I can help you with birthday-related conversations or calculations, but I won\'t be able to retrieve it from any existing records.'),
('01945e7a-9cf5-7b8c-8df0-64f825a8543e', 'f0033470-99d2-4aa1-af8a-79b9e29e9dbf', '2025-01-13 14:04:41', 'user', 'What did we talk about?'),
('01945e7a-a00d-787e-be7e-6d218a0e0b22', 'f0033470-99d2-4aa1-af8a-79b9e29e9dbf', '2025-01-13 14:04:42', 'assistant', 'We discussed two topics:\n\n1. The stock market crash of 1929: I provided an overview of the key factors that contributed to the crash, including overproduction, speculation, and weaknesses in the banking system.\n2. Your birthday: I mentioned that I don\'t have any information about your birthday, as I\'m a text-based AI assistant and don\'t have access to personal data or user profiles.'),
('01945ec0-7d45-7714-8d35-5853551098f3', 'f0cd3940-44ab-4f48-bcc9-d5f2dd3d833d', '2025-01-13 15:21:01', 'user', 'Can you introduce about COS40005?'),
('01945ec6-30d0-7039-8a34-9c8f21e9302e', '6776cdc6-cfa0-800f-bf3f-e3dedb47431f', '2025-01-13 15:27:15', 'user', 'Can you introduce about COS40005?'),
('01945ec6-3d48-78f7-8fea-a6f4a086386e', '6776cdc6-cfa0-800f-bf3f-e3dedb47431f', '2025-01-13 15:27:18', 'assistant', 'COS40005 is a unit of study at Swinburne University, specifically titled \"Computing Technology Project A\". Here\'s an introduction based on the provided unit outline:\n\n**Unit Overview**\nCOS40005 is a project-based unit that forms the first half of a two-semester capstone project. It aims to provide students with the skills to generate a computing technology solution to solve one or more industry challenges.\n\n**Key Features**\n\n* Duration: One semester\n* Credit Points: 12.5\n* Mode of Delivery: Blended (in-person and online)\n* Assessment: Portfolio-based, including participation, contribution, documentation, development, process, product, and presentation\n\n**Learning Outcomes**\nUpon completing this unit, students can:\n\n1. Review literature and investigate topic areas relating to computing technology\n2. Justify and manage risks in project planning and execution phases\n3. Apply research methods and skills to complete a research report\n4. Investigate the importance of research and data ethics\n5. Synthesize work related to computing technology projects relevant to their major\n6. Communicate within teams and stakeholders using appropriate verbal, written, and technological approaches\n\n**Graduate Attributes**\nThis unit contributes to the development of Swinburne Graduate Attributes, including:\n\n* GA1: Communication - Verbal communication\n* GA2: Communication - Communicating using different media\n* GA3: Teamwork - Collaboration and negotiation\n* GA4: Teamwork - Teamwork roles and processes\n\nLet me know if you have any specific questions or if there\'s anything else I can help you with!'),
('01945eca-902f-789d-a0e0-0ee74ef2c82f', '6776cdc6-cfa0-800f-bf3f-e3dedb47431f', '2025-01-13 15:32:01', 'user', 'What are the hurdle requirements to pass this subject?'),
('01945eca-9a99-71c7-b049-4e54eaa49bca', '6776cdc6-cfa0-800f-bf3f-e3dedb47431f', '2025-01-13 15:32:04', 'assistant', 'To pass the COS40005 unit, you must meet the following hurdle requirements:\n\n1. **Achieve an overall mark for the unit of 50% or more**: You need to obtain a minimum of 50% of the total marks available in the unit to pass.\n2. **Complete the project to an acceptable standard**: You must complete the project to a satisfactory level, as determined by the unit convenor. A rubric will be used to assess whether you have met the acceptable standard, and it will be available on Canvas.\n\nIf you do not successfully achieve the second hurdle requirement (completing the project to an acceptable standard), you will receive a maximum of 45% as your total mark for the unit.\n\nAdditionally, if you do not complete all the worklogs and do not submit a research report and all the group tasks, you will receive 0% (N) as your total mark for the unit.'),
('01945ecc-6153-71c6-8fac-bec80fbf1c8c', '6776cdc6-cfa0-800f-bf3f-e3dedb47431f', '2025-01-13 15:34:00', 'user', 'Who teaches this unit?'),
('01945ecc-6961-794d-852e-d986c8887b70', '6776cdc6-cfa0-800f-bf3f-e3dedb47431f', '2025-01-13 15:34:02', 'assistant', 'According to the unit outline, the Unit Convenor for COS40005 is:\n\n**Dr. Ly Quynh Tran**\nEmail: qly@swin.edu.au\n\nDr. Tran is available for consultation by email appointment.'),
('01945f22-0273-7fb5-9684-17f84ee78806', '01945f21-f105-7f4d-b69a-fff71fdbb61d', '2025-01-13 17:07:32', 'user', 'Can you introduce about COS40005?'),
('01945f22-0ead-7908-a4c7-fdf0d09f58cf', '01945f21-f105-7f4d-b69a-fff71fdbb61d', '2025-01-13 17:07:35', 'assistant', 'COS40005 is a unit of study at Swinburne University, titled \"Computing Technology Project A\". It is a project-based unit that forms the first half of a two-semester capstone project. Here are some key points about COS40005:\n\n**Unit Overview**\n\n* Unit Code: COS40005\n* Unit Title: Computing Technology Project A\n* Duration: One semester\n* Total Contact Hours: 48 hours\n* Credit Points: 12.5 credit points\n* Campus/Location: Da Nang\n* Mode of Delivery: Blended\n\n**Aims and Objectives**\n\n* The unit aims to provide students with the skills to generate a computing technology solution to solve one or more industry challenges.\n* Students will work individually or in teams to design and develop a computing technology project.\n* The unit focuses on the research and development stages of a year-long project, with an overall focus on computing technology innovation.\n\n**Assessment**\n\n* Students will be assessed on the basis of a portfolio, consisting of participation, contribution, documentation, development, process, product, and presentation.\n* To pass the unit, students must achieve an aggregate mark of 50% or more and complete the project to an acceptable standard.\n\n**Learning Outcomes**\n\n* Upon completing the unit, students will be able to:\n	1. Review literature and investigate topic areas relating to computing technology.\n	2. Justify and manage risks in the project planning and execution phases of computing technology projects.\n	3. Apply research methods and skills to complete a research report.\n	4. Investigate the importance of research and data ethics.\n	5. Synthesise work related to the computing technology projects relevant to their major.\n	6. Communicate within teams and stakeholders using appropriate verbal, written, and technological approaches.\n\n**Graduate Attributes**\n\n* The unit contributes to the development of the following Swinburne Graduate Attributes:\n	+ GA1 Communication - Verbal communication\n	+ GA2 Communication - Communicating using different media\n	+ GA3 Teamwork - Collaboration and negotiation\n	+ GA4 Teamwork – Teamwork roles and processes\n\nI hope this introduction provides a good overview of COS40005! Let me know if you have any further questions.'),
('01945f23-001f-7dd6-a50b-2fe04cf1a0f7', '01945f21-f105-7f4d-b69a-fff71fdbb61d', '2025-01-13 17:08:37', 'user', 'Can you introduce about SWE30003?'),
('01945f23-092d-7ee9-9290-ae194ae1e9ab', '01945f21-f105-7f4d-b69a-fff71fdbb61d', '2025-01-13 17:08:39', 'assistant', 'Unfortunately, I don\'t have any information about SWE30003 in the context provided. The context only mentions COS40005, which is a unit of study at Swinburne University. If you could provide more context or information about SWE30003, I\'d be happy to try and help you. Alternatively, if you have any questions about COS40005 or any other topic, feel free to ask!'),
('01945f28-6b91-7147-a7d2-3604ffd25584', '01945f21-f105-7f4d-b69a-fff71fdbb61d', '2025-01-13 17:14:32', 'user', 'Do you have information about SWE30003 now?'),
('01945f28-7c85-766d-9586-9760f04dd099', '01945f21-f105-7f4d-b69a-fff71fdbb61d', '2025-01-13 17:14:36', 'assistant', 'I have some information about SWE30003 now. Based on the excerpts provided, here\'s what I can tell you:\n\n**Unit Overview**\n\n* Unit Code: SWE30003\n* Unit Title: Digital Literacies 2 – Technical literacy (not explicitly mentioned, but inferred from the content)\n* Duration: One semester\n* Total Contact Hours: 36 hours (24 hours of lectures and 12 hours of tutorials)\n\n**Aims and Objectives**\n\n* The unit aims to provide students with the skills to identify, formulate, and analyze the requirements and constraints of a software system.\n* Students will learn about user goals, priorities, validation, analysis, abstractions, and patterns in software design.\n\n**Content**\n\n* The unit covers topics such as:\n	+ User goals and priorities\n	+ Constraints and validation\n	+ Analysis and abstractions\n	+ Patterns in software design\n	+ Software architectures and architectural styles\n	+ Design patterns and documentation\n\n**Assessment**\n\n* Students will be assessed on the basis of several tasks, including:\n	+ Weekly questions and answers (10%)\n	+ Requirements specification (20%)\n	+ Object-Oriented Design (25%)\n	+ Other assignments (weights not specified)\n\n**Learning Outcomes**\n\n* Upon completing the unit, students will be able to:\n	+ Identify, formulate, and analyze the requirements and constraints of a software system\n	+ Apply software design principles and patterns to develop software systems\n	+ Communicate software design decisions and trade-offs to stakeholders\n\n**Graduate Attributes**\n\n* The unit contributes to the development of the following Swinburne Graduate Attributes:\n	+ Not explicitly mentioned, but likely related to communication, teamwork, and problem-solving skills.\n\nPlease note that this information is based on the excerpts provided and may not be comprehensive or up-to-date. If you have any further questions or need more information, feel free to ask!'),
('01945f29-25f5-7e6b-bd68-9a71e57e465b', '01945f21-f105-7f4d-b69a-fff71fdbb61d', '2025-01-13 17:15:20', 'user', 'What is the unit name of SWE30003?'),
('01945f29-2ead-7796-858e-7dd494c244a1', '01945f21-f105-7f4d-b69a-fff71fdbb61d', '2025-01-13 17:15:22', 'assistant', 'According to the excerpts provided, the unit name of SWE30003 is \"Software Architectures and Design\".'),
('01945f29-543d-7e22-be12-b2d864b4a0ec', '01945f21-f105-7f4d-b69a-fff71fdbb61d', '2025-01-13 17:15:32', 'user', 'Can you provide more details about the \"User Goals and Priorities\" topic in the unit? '),
('01945f29-ccdb-73da-830c-91f041c1f816', '01945f21-f105-7f4d-b69a-fff71fdbb61d', '2025-01-13 17:16:03', 'assistant', 'According to the excerpts provided, the topic \"User Goals and Priorities\" is covered in the unit SWE30003 \"Software Architectures and Design\". Here\'s what I can infer about this topic:\n\n* The topic is likely introduced in the early weeks of the unit, possibly in Week 1 or Week 2, as part of the lectures on \"Introduction\" and \"Goal-Design Scale\".\n* The topic covers the concept of user goals and priorities in software design, which involves identifying and understanding the needs and objectives of the users of a software system.\n* The lectures and tutorials may explore how to analyze and prioritize user goals, and how to use this information to inform software design decisions.\n* The topic may also cover techniques for eliciting and documenting user goals and priorities, such as user interviews, surveys, and use cases.\n\nSome possible learning outcomes for this topic could include:\n\n* Understanding the importance of user goals and priorities in software design\n* Being able to identify and analyze user goals and priorities\n* Knowing how to prioritize user goals and make design decisions based on them\n* Being able to document and communicate user goals and priorities to stakeholders\n\nPlease note that this is just an inference based on the provided excerpts, and the actual content and learning outcomes of the topic may vary depending on the unit and the instructor. If you have any further questions or need more information, feel free to ask!'),
('01945f2b-ce2b-724a-b902-c1cbf58c0ffd', '01945f21-f105-7f4d-b69a-fff71fdbb61d', '2025-01-13 17:18:14', 'user', 'Who created this document?'),
('01945f2b-d7ab-78a7-bfa2-9fc8480cadac', '01945f21-f105-7f4d-b69a-fff71fdbb61d', '2025-01-13 17:18:16', 'assistant', 'The document appears to be a unit outline for a university course, specifically SWE30003 and COS40005, at Swinburne University. The creator of the document is likely to be the unit coordinator or instructor for the course, possibly with input from other academic staff members.\n\nIn the case of SWE30003, the unit coordinator is listed as Mr. Hoang Nhu, with the email address nhoang@swin.edu.au. However, it is not explicitly stated who created the document.\n\nFor COS40005, the document does not provide information on who created it.'),
('01945f2d-da97-79a3-ac3e-e832e0bc144e', '01945f21-f105-7f4d-b69a-fff71fdbb61d', '2025-01-13 17:20:28', 'user', 'what categories does this document belong to?'),
('01945f2d-e92e-78e4-a40c-47d6ea11d578', '01945f21-f105-7f4d-b69a-fff71fdbb61d', '2025-01-13 17:20:32', 'assistant', 'Based on the content and structure of the document, it appears to belong to the following categories:\n\n1. **Academic documents**: The document is a unit outline for a university course, which suggests that it is an academic document.\n2. **Educational materials**: The document provides information about the course, including learning outcomes, assessment tasks, and teaching schedules, which makes it an educational material.\n3. **University policies and procedures**: The document may also be considered a university policy or procedure document, as it outlines the rules and guidelines for the course, including assessment, submission, and academic integrity policies.\n4. **Course guides or syllabi**: The document is essentially a course guide or syllabus, providing students with essential information about the course, including its objectives, content, and requirements.\n\nOverall, the document can be categorized as an academic, educational, and administrative document, specifically designed for university students and staff.'),
('01945f54-202b-7756-90bb-46216251835b', '01945f53-d543-7ced-bbcb-96cdb1c90c9c', '2025-01-13 18:02:16', 'user', 'My name is Minh, nice to meet you.'),
('01945f54-274e-7028-bf53-40c164389a32', '01945f53-d543-7ced-bbcb-96cdb1c90c9c', '2025-01-13 18:02:18', 'assistant', 'Nice to meet you too, Minh. Is there something I can help you with or would you like to chat? I\'ve been provided with some unit outlines from Swinburne University, if you have any questions about those.'),
('01945f54-6143-75ef-a0ce-f7fb74cb4229', '01945f53-d543-7ced-bbcb-96cdb1c90c9c', '2025-01-13 18:02:33', 'user', 'Do you know my name?'),
('01945f54-6748-7e15-b61d-3f90a4e715b3', '01945f53-d543-7ced-bbcb-96cdb1c90c9c', '2025-01-13 18:02:35', 'assistant', 'Your name is Minh. You told me that when you introduced yourself.'),
('01945f56-f793-73b9-8af0-ece288781eaf', '01945f53-d543-7ced-bbcb-96cdb1c90c9c', '2025-01-13 18:05:23', 'user', 'Can you introduce about SWE30003?'),
('01945f56-fe50-7fb7-8c49-fb67216d6164', '01945f53-d543-7ced-bbcb-96cdb1c90c9c', '2025-01-13 18:05:24', 'assistant', 'SWE30003 is a unit at Swinburne University, and it\'s called \"Software Architectures and Design\". According to the unit outline, this unit aims to facilitate an in-depth study of state-of-the-art approaches and techniques for system design, with a special focus on the relationship between non-functional requirements and software architectures.\n\nThe unit covers topics such as:\n\n* Identifying, constructing, and justifying design abstractions\n* Analyzing system design in terms of common design patterns\n* Formulating and documenting architectural decisions\n* Recording and describing design decisions and structures using a contemporary modeling language\n\nThe unit also contributes to the development of several Swinburne Graduate Attributes, including communication, teamwork, and digital literacies.\n\nThe unit is delivered over 12 weeks, with a combination of lectures, tutorials, and assignments. The assessment includes a final test, group-based assignments, and weekly questions and answers submissions.\n\nIs there something specific you\'d like to know about SWE30003, Minh?'),
('01946387-4777-7d2c-a5d9-b930bf36ebf4', '01945f53-d543-7ced-bbcb-96cdb1c90c9c', '2025-01-14 13:36:38', 'user', 'What specific topics are covered in SWE30003?'),
('01946387-54f8-703e-b863-5d7e49bfe485', '01945f53-d543-7ced-bbcb-96cdb1c90c9c', '2025-01-14 13:36:41', 'assistant', 'According to the unit outline, SWE30003 covers the following specific topics:\n\n1. **User goals and priorities**: Identifying, formulating, and analyzing the requirements and constraints of a software system.\n2. **Constraints and priorities**: Understanding the importance of constraints and priorities in software design.\n3. **Validation and analysis**: Validating and analyzing software design decisions.\n4. **Abstractions and patterns**: Understanding abstractions in software, levels of abstraction, object-oriented abstractions, common patterns (structural and behavioral), pattern recognition, and identification.\n5. **Software architectures**: Decisions vs. structures, architectural patterns, documentation, and communication.\n6. **Architectural styles**: Message-driven architectures, client-server architectures, layered architectures, and service-oriented architecture (SOA).\n7. **Design patterns**: Detailed study of design patterns, including object-oriented design patterns.\n8. **Case studies**: Analyzing case studies in object design and architectural design.\n9. **Documentation and evaluation**: Documenting designs, evaluating design decisions, and using contemporary modeling languages.\n\nThese topics are covered over 12 weeks, with a combination of lectures, tutorials, and assignments. The unit aims to provide students with a deep understanding of software architectures and design principles, and how to apply them in real-world scenarios.\n\nIs there a specific topic you\'d like to know more about, Minh?'),
('019467e6-be0d-7a82-b338-3a3ab4d63ed8', '01945f53-d543-7ced-bbcb-96cdb1c90c9c', '2025-01-15 09:59:23', 'user', 'What are the key topics covered in SWE30003?'),
('0194da67-5507-7352-88a1-d9f0fb9b3cab', '0194da67-4e79-76c4-a632-8ff60b9fcf4a', '2025-02-06 15:36:33', 'user', 'How to allow multiline text in a table cell in Markdown syntax?'),
('0194da67-64a7-7c93-9946-c1c1a39644e4', '0194da67-4e79-76c4-a632-8ff60b9fcf4a', '2025-02-06 15:36:37', 'assistant', 'To allow multiline text in a table cell in Markdown syntax, you can use HTML line breaks (`<br>`) or separate the lines with a space and a newline. However, the most common and compatible way is to use HTML line breaks (`<br>`).\n\nHere\'s an example:\n\n```markdown\n| Column 1 | Column 2 |\n|----------|----------|\n| Cell 1   | Cell 2 with <br> multiple lines|\n| Cell 3   | Cell 4   |\n```\n\nIn this example, \"Cell 2 with multiple lines\" will be displayed as two separate lines within the same table cell.\n\nAlternatively, you can use a space and a newline to separate the lines, like this:\n\n```markdown\n| Column 1 | Column 2 |\n|----------|----------|\n| Cell 1   | Cell 2 with \n multiple lines|\n| Cell 3   | Cell 4   |\n```\n\nHowever, this method may not work in all Markdown parsers, so using HTML line breaks (`<br>`) is generally more reliable.\n\nReferences:\nNone'),
('0194da68-e6da-7790-b354-758e6a30813b', '0194da67-4e79-76c4-a632-8ff60b9fcf4a', '2025-02-06 15:38:16', 'user', 'Do you have any relevant documents to it?'),
('0194da68-f5b7-7642-ae6d-9a8d6a263824', '0194da67-4e79-76c4-a632-8ff60b9fcf4a', '2025-02-06 15:38:19', 'assistant', 'No, I don\'t have any relevant documents to the question about multiline text in Markdown syntax. The information provided was based on general knowledge of Markdown syntax.\n\nReferences:\nNone'),
('0194da69-8faf-7638-aeeb-744cec4c48ca', '0194da69-8b7c-7081-9283-0dc94d907fc0', '2025-02-06 15:38:59', 'user', 'How to allow multiline text in a table cell in Markdown syntax?'),
('0194da69-9f91-7568-ac12-0d5aed632daf', '0194da69-8b7c-7081-9283-0dc94d907fc0', '2025-02-06 15:39:03', 'assistant', 'To allow multiline text in a table cell in Markdown syntax, you can use the `<pre>` tag or the backtick (`` ` ``) inside the table cell. \n\nHere\'s an example using the `<pre>` tag:\n\n```markdown\n| Column 1 | Column 2 |\n|---------|----------|\n| Cell 1  | <pre>Cell 2 line 1<br/>Cell 2 line 2</pre>|\n```\n\nAlternatively, you can use the backtick (`` ` ``) inside the table cell:\n\n```markdown\n| Column 1 | Column 2 |\n|---------|----------|\n| Cell 1  | ```Cell 2 line 1\nCell 2 line 2```|\n```\n\nHowever, the most common and recommended approach is to use the backtick (`` ` ``) with the `<pre>` tag for better formatting and readability:\n\n```markdown\n| Column 1 | Column 2 |\n|---------|----------|\n| Cell 1  | <pre>```\nCell 2 line 1\nCell 2 line 2\n``</pre>|\n```\n\nThis will allow you to have multiline text in a table cell using Markdown syntax.\n\nReferences:\n* Markdown multiline code blocks in tables when rows have to be specified with one-liners (Minh Nguyễn, 2025-02-06, https://stackoverflow.com/questions/24190085/markdown-multiline-code-blocks-in-tables-when-rows-have-to-be-specified-with-one)'),
('0194da6b-9778-7540-b5ab-53b2a579b05a', '0194da67-4e79-76c4-a632-8ff60b9fcf4a', '2025-02-06 15:41:12', 'user', 'Do you have any relevant documents about multiline text in a table cell in Markdown syntax?'),
('0194da6b-a81b-7109-aac9-69c723f24098', '0194da67-4e79-76c4-a632-8ff60b9fcf4a', '2025-02-06 15:41:16', 'assistant', 'Yes, I have a relevant document about multiline text in a table cell in Markdown syntax. \n\nTo allow multiline text in a table cell in Markdown syntax, you can use HTML line breaks (`<br>`) or separate the lines with a space and a newline. However, the most common and compatible way is to use HTML line breaks (`<br>`).\n\nHere\'s an example:\n\n```markdown\n| Column 1 | Column 2 |\n|----------|----------|\n| Cell 1   | Cell 2 with <br> multiple lines|\n| Cell 3   | Cell 4   |\n```\n\nIn this example, \"Cell 2 with multiple lines\" will be displayed as two separate lines within the same table cell.\n\nAlternatively, you can use a space and a newline to separate the lines, like this:\n\n```markdown\n| Column 1 | Column 2 |\n|----------|----------|\n| Cell 1   | Cell 2 with \n multiple lines|\n| Cell 3   | Cell 4   |\n```\n\nHowever, this method may not work in all Markdown parsers, so using HTML line breaks (`<br>`) is generally more reliable.\n\nReferences:\nNguyễn, M. (2025, February 6). Markdown multiline code blocks in tables when rows have to be specified with one-liners. https://stackoverflow.com/questions/24190085/markdown-multiline-code-blocks-in-tables-when-rows-have-to-be-specified-with-one'),
('0194da6c-1f91-7486-843b-6df69c2595fd', '0194da67-4e79-76c4-a632-8ff60b9fcf4a', '2025-02-06 15:41:47', 'user', 'Help me summary the details of worklog week 2 of COS40005'),
('0194da6c-2d25-7872-a093-df4b08576a78', '0194da67-4e79-76c4-a632-8ff60b9fcf4a', '2025-02-06 15:41:50', 'assistant', 'Based on the provided context, here is a summary of the details of Worklog Week 2 of COS40005:\n\n* The worklog is for Week 2 of the COS40005 unit.\n* The unit outline mentions that late submissions will be penalized 10% of the achieved mark for each working day, up to a maximum of 5 working days. After 5 working days, a zero result will be recorded.\n* The outline also emphasizes the importance of referencing and academic integrity, and provides a link to the Swinburne University library\'s referencing guide.\n* The unit has a groupwork component, and group submissions must be submitted with an Assignment Cover Sheet signed by all group members.\n* The recommended reading materials for the unit include books on software requirements, software architecture, and design patterns.\n\nReferences:\nNone'),
('0194da73-2881-78c1-8848-0820fee706a7', '0194da67-4e79-76c4-a632-8ff60b9fcf4a', '2025-02-06 15:49:28', 'user', 'Help me summary the details of worklog week 2 of COS40005, I\'ve just uploaded a new doc.'),
('0194da73-36d3-746e-b2bd-97a9c65a3e0b', '0194da67-4e79-76c4-a632-8ff60b9fcf4a', '2025-02-06 15:49:31', 'assistant', 'Based on the provided context, here is a summary of the details of Worklog Week 2 of COS40005:\n\n* The worklog is for Week 2 of the COS40005 unit, which covers Digital Literacies 2 – Technical literacy.\n* The unit outline for SWE30003 is provided, which includes the unit\'s learning outcomes, assessment tasks, and teaching schedule.\n* The week\'s topics include:\n	+ Lecture: Goal-Design Scale, User Tasks\n	+ Tutorial: Software Design Issues\n	+ Assignment: Group Formation\n* The unit outline also mentions that feedback from previous students has resulted in improvements, including making all assignments group work, clarifying expectations, and introducing new architecture styles.\n\nReferences:\nNguyen, M. (2025, January 22). COS40005 Worklog - Week 2. Retrieved from <coroutine object DocumentService.generate_document_url at 0x000001CF59A91990>'),
('0194da74-6f41-7223-87a7-33a2c84a8c8c', '0194da67-4e79-76c4-a632-8ff60b9fcf4a', '2025-02-06 15:50:51', 'user', 'Help me summary the details of worklog week 2 of COS40005, I\'ve just uploaded a new doc.'),
('0194da74-8942-7505-abe1-61fdeab70edd', '0194da67-4e79-76c4-a632-8ff60b9fcf4a', '2025-02-06 15:50:58', 'assistant', 'Based on the provided context, here is a summary of the details of Worklog Week 2 of COS40005:\n\n* The worklog is for Week 2 of the COS40005 unit, which covers Digital Literacies 2 – Technical literacy.\n* The unit outline for SWE30003 is provided, which includes the unit\'s learning outcomes, assessment tasks, and teaching schedule.\n* The week\'s topics include:\n	+ Lecture: Goal-Design Scale, User Tasks\n	+ Tutorial: Software Design Issues\n	+ Assignment: Group Formation\n* The unit outline also mentions that feedback from previous students has resulted in improvements, including making all assignments group work, clarifying expectations, and introducing new architecture styles.\n\nReferences:\nNguyen, M. (2025, January 22). COS40005 Worklog - Week 2. https://rikkeisoft-s3.s3.ap-southeast-2.amazonaws.com/uploads/d21694ef-973b-41d1-97b8-178dce535808.pdf?response-content-disposition=attachment%3B%20filename%3DCOS40005%20Worklog%20-%20Week%202.pdf&AWSAccessKeyId=AKIAXNGUVTVY3JHPYK5E&Signature=ZEhWvCtrXmwv8fHoA9Sp6n2Yab4%3D&Expires=1738835455'),
('0194da81-e4d3-70c0-97a8-959cf238ea77', '0194da81-e053-7c2e-8d5d-555b3892467b', '2025-02-06 16:05:33', 'user', 'Help me summary the details of worklog week 2 of COS40005.');
INSERT INTO `messages` (`id`, `chat_id`, `time`, `role`, `content`) VALUES
('0194da82-057e-74c2-862e-3e335343550a', '0194da81-e053-7c2e-8d5d-555b3892467b', '2025-02-06 16:05:42', 'assistant', 'Based on the provided context, the COS40005 Worklog - Week 2 document contains information about the unit outline, including assessment details and late submission policies. Here\'s a summary of the key points:\n\n* Late submission policy: a penalty of 10% of the achieved mark for each working day the task is late, up to a maximum of 5 working days. After 5 working days, a zero result will be recorded.\n* Referencing: students are required to provide references whenever they include information from other sources in their work and acknowledge when they have used Artificial Intelligence (AI) tools.\n* Groupwork guidelines: group assignments are the collective responsibility of the entire group, and if one member is temporarily unable to contribute, the group should be able to reallocate responsibilities to keep to schedule.\n* Assessment overview: the unit has several assessments, including weekly questions and answers, requirements specification, object-oriented design, and more.\n\nPlease note that the provided context does not contain a detailed worklog for Week 2 of COS40005. The document seems to be a unit outline, and the worklog details are not explicitly mentioned.\n\nReferences:\n* COS40005 Worklog - Week 2 (Nguyen Minh, 2025) \n  Preview: https://docs.google.com/gview?embedded=true&url=https%3A%2F%2Frikkeisoft-s3.s3.ap-southeast-2.amazonaws.com%2Fuploads%2Fd21694ef-973b-41d1-97b8-178dce535808.pdf%3Fresponse-content-disposition%3Dattachment%253B%2520filename%253DCOS40005%2520Worklog%2520-%2520Week%25202.pdf%26AWSAccessKeyId%3DAKIAXNGUVTVY3JHPYK5E%26Signature%3DkQXK9i5BCCkI%252B8ycbzGoARIw7aY%253D%26Expires%3D1738836338 \n  Download: https://rikkeisoft-s3.s3.ap-southeast-2.amazonaws.com/uploads/d21694ef-973b-41d1-97b8-178dce535808.pdf?response-content-disposition=attachment%3B%20filename%3DCOS40005%20Worklog%20-%20Week%202.pdf&AWSAccessKeyId=AKIAXNGUVTVY3JHPYK5E&Signature=kQXK9i5BCCkI%2B8ycbzGoARIw7aY%3D&Expires=1738836338'),
('0194da84-25bb-7a84-b7bb-b5a70a8ecd47', '0194da84-2162-7b61-80e8-756bb35ed772', '2025-02-06 16:08:01', 'user', 'Help me summary the details of worklog week 2 of COS40005.'),
('0194da84-3b17-7f00-b227-17303f3b3aed', '0194da84-2162-7b61-80e8-756bb35ed772', '2025-02-06 16:08:07', 'assistant', 'Based on the provided context, the COS40005 Worklog - Week 2 includes the following details:\n\n* A penalty of 10% of the achieved mark for each working day the task is late, up to a maximum of 5 working days, after which a zero result will be recorded.\n* No late submission will be granted for the Weekly Question and Answer submission.\n* The importance of referencing to avoid breaching academic integrity, including the use of Artificial Intelligence (AI) tools.\n* Groupwork guidelines, emphasizing the collective responsibility of the entire group and the need for members to notify the Unit Convenor or relevant tutor in case of any issues.\n* Recommended reading materials, including various books on software requirements, design, and architecture.\n\nReferences:\n* COS40005 Worklog - Week 2 ([Preview](https://docs.google.com/gview?embedded=true&url=https%3A%2F%2Frikkeisoft-s3.s3.ap-southeast-2.amazonaws.com%2Fuploads%2Fd21694ef-973b-41d1-97b8-178dce535808.pdf%3Fresponse-content-disposition%3Dattachment%253B%2520filename%253DCOS40005%2520Worklog%2520-%2520Week%25202.pdf%26AWSAccessKeyId%3DAKIAXNGUVTVY3JHPYK5E%26Signature%3DBDpttgJsPLnwHBjNi2YFna%252F0rpw%253D%26Expires%3D1738836484) | [Download](https://rikkeisoft-s3.s3.ap-southeast-2.amazonaws.com/uploads/d21694ef-973b-41d1-97b8-178dce535808.pdf?response-content-disposition=attachment%3B%20filename%3DCOS40005%20Worklog%20-%20Week%202.pdf&AWSAccessKeyId=AKIAXNGUVTVY3JHPYK5E&Signature=BDpttgJsPLnwHBjNi2YFna%2F0rpw%3D&Expires=1738836484)) by Nguyen Minh, 2025-01-22.'),
('0194da8b-6372-7280-bb65-d1919e6e6eb6', '0194da8b-5efe-7b49-9893-a52fc57ff89d', '2025-02-06 16:15:56', 'user', 'Help me summary the details of worklog week 2 of COS40005.'),
('0194da8b-7a95-7dd2-bed4-079f42627eb5', '0194da8b-5efe-7b49-9893-a52fc57ff89d', '2025-02-06 16:16:02', 'assistant', 'Based on the provided worklog for Week 2 of COS40005, here\'s a summary of the details:\n\nThe worklog covers the period from January 6th, 2025, to January 12th, 2025. During this week, the student, Nguyen Thi Thanh Minh, worked on several tasks related to the SmartHealth project. The tasks completed include:\n\n1. Attending a workshop on project inception and planning (2 hours)\n2. Conducting a SWOT analysis for a hypothetical project scenario (1.5 hours)\n3. Finalizing the team plan and researching (1.5 hours)\n4. Developing the project charter for SmartHealth (2 hours)\n5. Creating an initial project plan draft (2 hours)\n6. Conducting independent research on project inception methods (1.5 hours)\n\nThe total time spent on these tasks was 10.5 hours. The student also planned tasks for the next week, which include meeting the client to finalize project requirements, conducting research on AI tools for personalized health, and revising the project plan based on supervisor feedback.\n\nThe student reflected on the key tasks done, things learned, and issues faced during the week. They noted the importance of a project charter, a well-drafted project plan, and SWOT analysis in the early phases of a project.\n\nReferences:\n* COS40005 Worklog - Week 2 (<a href=\"https://docs.google.com/gview?embedded=true&url=https%3A%2F%2Frikkeisoft-s3.s3.ap-southeast-2.amazonaws.com%2Fuploads%2Fdd43369c-575c-425a-aaa9-3ada0486cfa3.pdf%3Fresponse-content-disposition%3Dattachment%253B%2520filename%253DCOS40005%2520Worklog%2520-%2520Week%25202.pdf%26AWSAccessKeyId%3DAKIAXNGUVTVY3JHPYK5E%26Signature%3DKCQExqQgHSnf83XGmxzR2oSrn8E%253D%26Expires%3D1738836958\" target=\"_blank\">Preview</a>, <a href=\"https://rikkeisoft-s3.s3.ap-southeast-2.amazonaws.com/uploads/dd43369c-575c-425a-aaa9-3ada0486cfa3.pdf?response-content-disposition=attachment%3B%20filename%3DCOS40005%20Worklog%20-%20Week%202.pdf&AWSAccessKeyId=AKIAXNGUVTVY3JHPYK5E&Signature=KCQExqQgHSnf83XGmxzR2oSrn8E%3D&Expires=1738836958\" target=\"_blank\">Download</a>) by Nguyen Minh, 2025-01-22.'),
('0194da93-b4da-798c-a731-4ea05755dcc3', '0194da93-b057-7c9e-9e0b-137d7c305d96', '2025-02-06 16:25:01', 'user', 'Minh\nHelp me summary the details of worklog week 2 of COS40005.'),
('0194da93-c02f-7c8a-b199-64333323dd7b', '0194da93-b057-7c9e-9e0b-137d7c305d96', '2025-02-06 16:25:04', 'assistant', 'I\'m happy to help you, Minh. However, I don\'t have any information about the worklog week 2 of COS40005. Could you please provide more context or details about what COS40005 is and what kind of worklog you are referring to? I\'ll do my best to assist you.\n\nIf you have any relevant documents or sources, please let me know and I\'ll be happy to help you summarize the details.\n\nReferences: None'),
('0194db73-8a79-7faf-bdcb-272056d3200a', '0194da8b-5efe-7b49-9893-a52fc57ff89d', '2025-02-06 20:29:30', 'user', 'give me new link'),
('0194db73-e9fb-7a38-a5b0-350e6697ddf1', '0194da8b-5efe-7b49-9893-a52fc57ff89d', '2025-02-06 20:29:54', 'assistant', 'It seems that I don\'t have any information about the worklog week 2 of COS40005. The provided context doesn\'t contain any details about this specific topic.\n\nIf you\'re looking for information about COS40005, I can try to help you with the provided context. The COS40005 Sprint 1 Project Specification document is available, and I can provide you with a summary of its content.\n\nReferences:\n* COS40005 Sprint 1 Project Specification (<a href=\"https://docs.google.com/gview?embedded=true&url=https%3A%2F%2Frikkeisoft-s3.s3.ap-southeast-2.amazonaws.com%2Fuploads%2F88062a21-84f2-4015-9f5c-200fcdda6c33.docx%3Fresponse-content-disposition%3Dattachment%253B%2520filename%253DCOS40005%2520Sprint%25201%2520Project%2520Specification.docx%26AWSAccessKeyId%3DAKIAXNGUVTVY3JHPYK5E%26Signature%3D65MvwtFs3qI0UG6EKUzYsLCZ6iI%253D%26Expires%3D1738852187\" target=\"_blank\">Preview</a>, <a href=\"https://rikkeisoft-s3.s3.ap-southeast-2.amazonaws.com/uploads/88062a21-84f2-4015-9f5c-200fcdda6c33.docx?response-content-disposition=attachment%3B%20filename%3DCOS40005%20Sprint%201%20Project%20Specification.docx&AWSAccessKeyId=AKIAXNGUVTVY3JHPYK5E&Signature=65MvwtFs3qI0UG6EKUzYsLCZ6iI%3D&Expires=1738852187\" target=\"_blank\">Download</a>) by Minh Nguyen, 2025-02-06.'),
('0194e99d-9f3a-74fb-b0e1-26d8fdb85bfa', '0194da8b-5efe-7b49-9893-a52fc57ff89d', '2025-02-09 07:30:09', 'user', 'send me a high five!'),
('0194e99d-a7f5-7816-864a-200c9822abf3', '0194da8b-5efe-7b49-9893-a52fc57ff89d', '2025-02-09 07:30:11', 'assistant', 'I\'d be happy to send you a virtual high five! ***HIGH FIVE*** Unfortunately, I couldn\'t find any relevant information to provide an answer with references. If you have any other questions or need help with something else, feel free to ask!');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `name`, `description`) VALUES
(1, 'system_admin', 'System administrator'),
(2, 'admin', 'Administrator'),
(3, 'employee', 'Regular employee');

-- --------------------------------------------------------

--
-- Table structure for table `sso`
--

CREATE TABLE `sso` (
  `user_id` char(36) NOT NULL,
  `provider` enum('google','microsoft') NOT NULL,
  `sub` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `sso`
--

INSERT INTO `sso` (`user_id`, `provider`, `sub`) VALUES
('e524734c-549c-44b4-84d2-5f144613ab1c', 'google', '106272218561460451545'),
('1642be2a-e3a9-4679-87eb-1365f9f470d0', 'google', '107360694239114519362'),
('f7e0386e-8e56-464b-82ef-19747f6a9bae', 'microsoft', 'AAAAAAAAAAAAAAAAAAAAAAGWQBsfLK99T6YSqJXyY4s'),
('52676658-2055-4e53-b7b2-cab4957aad0b', 'microsoft', 'suS03TZEAYkMuTigHe9LvwWrwcsPnWkDObw2SCrrITM');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` char(36) NOT NULL,
  `email` varchar(100) NOT NULL,
  `firstname` varchar(50) NOT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` char(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `avatar_url` text,
  `created_time` datetime NOT NULL,
  `username_last_changed` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `firstname`, `lastname`, `username`, `password`, `avatar_url`, `created_time`, `username_last_changed`) VALUES
('1642be2a-e3a9-4679-87eb-1365f9f470d0', '104169617@student.swin.edu.au', 'Nguyen', 'Minh', '', '$2b$12$gUr08tFVl1Fvae78DwrEAefIXQGxYdCeqe6TERd.kBoDlkr3hUVNq', 'https://lh3.googleusercontent.com/a/ACg8ocIeYtfsHCc2K2Ujapow2nSd6R3zr8kEx_YgWIuv_FnsoAkoWB4=s360-c-no', '2025-01-18 15:00:09', NULL),
('52676658-2055-4e53-b7b2-cab4957aad0b', 'minhntt3_tts@rikkeisoft.com', 'Minh', 'Nguyen Thi Thanh', NULL, NULL, 'https://rikkeigpt-bucket.s3.amazonaws.com/avatars/52676658-2055-4e53-b7b2-cab4957aad0b.jpg', '2025-02-06 14:35:26', NULL),
('86ce47d5-0bf4-47c4-adb4-2be068e73580', 'hoang@gmail.com', 'Hoang', 'Duong', 'hoangdvm', '$2b$12$A2z0GT136/XX.7a5MeL3eOlYWX4AWoPCsnm738iRxFZcn2Gk2oN8W', 'https://rikkeigpt-bucket.s3.ap-southeast-2.amazonaws.com/avatars/86ce47d5-0bf4-47c4-adb4-2be068e73580.png', '2025-01-16 10:41:26', '2025-01-16 10:41:26'),
('c24d9619-848d-4af6-87c8-718444421762', 'minh@gmail.com', 'Minh', 'Nguyen', 'tminh1512', '$2b$12$4aI1752f0eN4YZbjdB5PQeIwzv5GDs/waVMGZFTBPNyuJUm7jBiS.', 'https://rikkeigpt-bucket.s3.ap-southeast-2.amazonaws.com/avatars/c24d9619-848d-4af6-87c8-718444421762.jpg', '2025-01-16 10:41:26', '2025-01-16 10:41:26'),
('e524734c-549c-44b4-84d2-5f144613ab1c', 'minhnttswd00087@fpt.edu.vn', 'Nguyen Thi Thanh Minh', '(Swinburne DN)', NULL, NULL, 'https://lh3.googleusercontent.com/a/ACg8ocL_9noZAziIEx_bV9AJ3vXww3vdEZu_3ojXRoih7FvL_SJY4A=s96-c', '2025-02-06 13:01:16', NULL),
('f7e0386e-8e56-464b-82ef-19747f6a9bae', 'thanhminh.nt.1512@gmail.com', 'Minh', 'Nguyễn', NULL, NULL, 'https://rikkeigpt-bucket.s3.ap-southeast-2.amazonaws.com/avatars/microsoft_AAAAAAAAAAAAAAAAAAAAAAGWQBsfLK99T6YSqJXyY4s.jpg', '2025-02-06 14:40:39', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_roles`
--

CREATE TABLE `user_roles` (
  `user_id` char(36) NOT NULL,
  `role_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user_roles`
--

INSERT INTO `user_roles` (`user_id`, `role_id`) VALUES
('c24d9619-848d-4af6-87c8-718444421762', 1),
('86ce47d5-0bf4-47c4-adb4-2be068e73580', 2),
('c24d9619-848d-4af6-87c8-718444421762', 2),
('1642be2a-e3a9-4679-87eb-1365f9f470d0', 3),
('52676658-2055-4e53-b7b2-cab4957aad0b', 3),
('86ce47d5-0bf4-47c4-adb4-2be068e73580', 3),
('c24d9619-848d-4af6-87c8-718444421762', 3),
('e524734c-549c-44b4-84d2-5f144613ab1c', 3),
('f7e0386e-8e56-464b-82ef-19747f6a9bae', 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `chats`
--
ALTER TABLE `chats`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `documents`
--
ALTER TABLE `documents`
  ADD PRIMARY KEY (`id`),
  ADD KEY `creator` (`creator`),
  ADD KEY `uploader` (`uploader`);

--
-- Indexes for table `document_categories`
--
ALTER TABLE `document_categories`
  ADD PRIMARY KEY (`document_id`,`category_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `document_status`
--
ALTER TABLE `document_status`
  ADD PRIMARY KEY (`document_id`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `chat_id` (`chat_id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `sso`
--
ALTER TABLE `sso`
  ADD PRIMARY KEY (`user_id`,`provider`),
  ADD UNIQUE KEY `provider` (`provider`,`sub`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `user_roles`
--
ALTER TABLE `user_roles`
  ADD PRIMARY KEY (`user_id`,`role_id`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `chats`
--
ALTER TABLE `chats`
  ADD CONSTRAINT `chats_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `documents`
--
ALTER TABLE `documents`
  ADD CONSTRAINT `documents_ibfk_1` FOREIGN KEY (`creator`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `documents_ibfk_2` FOREIGN KEY (`uploader`) REFERENCES `users` (`id`);

--
-- Constraints for table `document_categories`
--
ALTER TABLE `document_categories`
  ADD CONSTRAINT `document_categories_ibfk_1` FOREIGN KEY (`document_id`) REFERENCES `documents` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `document_categories_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `document_status`
--
ALTER TABLE `document_status`
  ADD CONSTRAINT `document_status_ibfk_1` FOREIGN KEY (`document_id`) REFERENCES `documents` (`id`);

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`chat_id`) REFERENCES `chats` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `sso`
--
ALTER TABLE `sso`
  ADD CONSTRAINT `sso_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `user_roles`
--
ALTER TABLE `user_roles`
  ADD CONSTRAINT `user_roles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
