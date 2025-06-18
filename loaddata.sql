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
('Eve', 'Turner', 'eve@example.com', 'Data analyst turned coder.', 'eve_t', 'password123', 'https://picsum.photos/200?5', '2024-06-12', 1);

INSERT INTO Posts (user_id, category_id, title, publication_date, image_url, content, approved) VALUES
(1, 1, 'Launch Day Recap', '2024-12-15', 'https://picsum.photos/300?1', 'Our platform went live!', 1),
(2, 1, 'Why I Love APIs', '2023-09-10', 'https://picsum.photos/300?2', 'Let’s talk REST and GraphQL.', 1),
(3, 1, 'Refactoring Tips', '2025-06-01', 'https://picsum.photos/300?3', 'Make your code cleaner.', 0),
(4, 1, 'Dev Tools I Use Daily', '2025-06-16', 'https://picsum.photos/300?4', 'A deep dive into my setup.', 1),
(5, 1, 'Under Review: Async JS', '2025-06-17', 'https://picsum.photos/300?5', 'Promises vs async/await.', 0);

INSERT INTO Comments (post_id, author_id, content) VALUES
(1, 2, 'Great summary!'),
(2, 3, 'Very insightful.'),
(3, 1, 'Needs some editing.'),
(4, 5, 'I love VSCode too!'),
(5, 2, 'Can’t wait to read more.');

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

