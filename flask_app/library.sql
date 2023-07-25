-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema library_app
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `library_app` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `library_app` ;

-- -----------------------------------------------------
-- Table `library_app`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library_app`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(20) NULL DEFAULT NULL,
  `email` VARCHAR(150) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `real_name` VARCHAR(100) NULL DEFAULT NULL,
  `gender` VARCHAR(45) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `password_UNIQUE` (`password` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `library_app`.`books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library_app`.`books` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(200) NULL DEFAULT NULL,
  `author` VARCHAR(200) NULL DEFAULT NULL,
  `pages` INT NULL DEFAULT NULL,
  `publisher` VARCHAR(100) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `library_app`.`saves`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `library_app`.`saves` (
  `user_id` INT NOT NULL,
  `book_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  INDEX `fk_saves_books1_idx` (`book_id` ASC) VISIBLE,
  INDEX `fk_saves_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_saves_books1`
    FOREIGN KEY (`book_id`)
    REFERENCES `library_app`.`books` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_saves_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `library_app`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
