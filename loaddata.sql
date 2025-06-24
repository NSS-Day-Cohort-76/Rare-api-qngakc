-- Run this block if you already have a database and need to re-create it
DELETE FROM Users;


DROP TABLE IF EXISTS PostTags;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS PostReactions;
DROP TABLE IF EXISTS Reactions;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Subscriptions;
DROP TABLE IF EXISTS DemotionQueue;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Users;
-- End block


CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Tags ('label') VALUES ('JavaScript');
INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');

INSERT INTO Users (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active) VALUES
('Alice', 'Smith', 'alice@example.com', 'Lover of front-end design.', 'alice_s', 'password123', 'https://picsum.photos/200?1', '2024-03-01', 1),
('Bob', 'Johnson', 'bob@example.com', 'Back-end wizard.', 'bob_j', 'password123', 'https://picsum.photos/200?2', '2023-11-15', 1),
('Clara', 'Nguyen', 'clara@example.com', 'Full-stack dev and mentor.', 'clara_n', 'password123', 'https://picsum.photos/200?3', '2022-08-20', 1),
('David', 'Lee', 'david@example.com', 'Tech blogger & gamer.', 'david_l', 'password123', 'https://picsum.photos/200?4', '2025-01-10', 0),
('Eve', 'Turner', 'eve@example.com', 'Data analyst turned coder.', 'eve_t', 'password123', 'https://picsum.photos/200?5', '2024-06-12', 1),
('Fiona', 'Adams', 'fiona@example.com', 'UX researcher and cat mom.', 'fiona_a', 'password123', 'https://picsum.photos/200?6', '2024-05-10', 1),
('George', 'Baker', 'george@example.com', 'DevOps enthusiast.', 'george_b', 'password123', 'https://picsum.photos/200?7', '2023-04-22', 1),
('Hannah', 'Chen', 'hannah@example.com', 'New to coding but loving it!', 'hannah_c', 'password123', 'https://picsum.photos/200?8', '2025-02-01', 1),
('Ian', 'Davis', 'ian@example.com', 'Cybersecurity student.', 'ian_d', 'password123', 'https://picsum.photos/200?9', '2024-09-18', 0),
('Jasmine', 'Evans', 'jasmine@example.com', 'Python dev and blogger.', 'jasmine_e', 'password123', 'https://picsum.photos/200?10', '2023-12-05', 1);

INSERT INTO Posts (
  user_id,
  category_id,
  title,
  publication_date,
  image_url,
  content,
  approved
) VALUES (
  1,
  1,
  'Test title',
  CURRENT_TIMESTAMP,
  'https://example.com/image.jpg',
  'Fake post content.',
  1
);
INSERT INTO Posts (user_id, category_id, title, publication_date, image_url, content, approved) VALUES
(1, 1, 'Launch Day Recap', '2024-12-15', 'https://picsum.photos/300?1', 'Our platform went live!', 1),
(2, 1, 'Why I Love APIs', '2023-09-10', 'https://picsum.photos/300?2', 'Let’s talk REST and GraphQL.', 1),
(3, 1, 'Refactoring Tips', '2025-06-01', 'https://picsum.photos/300?3', 'Make your code cleaner.', 0),
(4, 1, 'Dev Tools I Use Daily', '2025-06-16', 'https://picsum.photos/300?4', 'A deep dive into my setup.', 1),
(5, 1, 'Under Review: Async JS', '2025-06-17', 'https://picsum.photos/300?5', 'Promises vs async/await.', 0),
(6, 2, 'Journey into UX', '2024-06-10', 'https://picsum.photos/300?6', 'Sharing what I learned about user interviews.', 1),
(7, 3, 'CI/CD in Practice', '2023-05-03', 'https://picsum.photos/300?7', 'Automating deployments the right way.', 1),
(8, 1, 'Learning JavaScript', '2025-03-11', 'https://picsum.photos/300?8', 'What surprised me about JavaScript.', 0),
(9, 4, 'Staying Safe Online', '2024-11-27', 'https://picsum.photos/300?9', 'Simple tips to improve your security.', 1),
(10, 1, 'Why I Switched to FastAPI', '2024-01-20', 'https://picsum.photos/300?10', 'Better performance and async support.', 1);

INSERT INTO Comments (post_id, author_id, content) VALUES
(1, 2, 'Great summary!'),
(2, 3, 'Very insightful.'),
(3, 1, 'Needs some editing.'),
(4, 5, 'I love VSCode too!'),
(5, 2, 'Can’t wait to read more.'),
(6, 1, 'Really useful UX advice, thanks!'),
(7, 3, 'DevOps is so underrated.'),
(8, 2, 'We all struggle at first—keep going!'),
(9, 4, 'Cybersecurity is everyone’s job.'),
(10, 5, 'FastAPI is amazing! Great post.');

INSERT INTO PostReactions (user_id, reaction_id, post_id) VALUES
(1, 1, 2),
(2, 1, 1),
(3, 1, 4);

INSERT INTO PostTags (post_id, tag_id) VALUES
(2, 1),
(3, 1),
(5, 1);

INSERT INTO Subscriptions (follower_id, author_id, created_on) VALUES
(1, 2, '2024-12-01'),
(3, 1, '2025-01-01'),
(2, 5, '2025-06-01');



