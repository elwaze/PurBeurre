-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema OFF
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `OFF` ;

-- -----------------------------------------------------
-- Schema OFF
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `OFF` DEFAULT CHARACTER SET utf8 ;
USE `OFF` ;

-- -----------------------------------------------------
-- Table `OFF`.`category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OFF`.`category` ;

CREATE TABLE IF NOT EXISTS `OFF`.`category` (
  `name` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`name`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OFF`.`product`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OFF`.`product` ;

CREATE TABLE IF NOT EXISTS `OFF`.`product` (
  `link` VARCHAR(256) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `nutriscore` VARCHAR(1) NOT NULL,
  `category_name` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`link`, `category_name`),
  INDEX `fk_product_category1_idx` (`category_name` ASC) VISIBLE,
  UNIQUE INDEX `link_UNIQUE` (`link` ASC) VISIBLE,
  CONSTRAINT `fk_product_category1`
    FOREIGN KEY (`category_name`)
    REFERENCES `OFF`.`category` (`name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OFF`.`store`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OFF`.`store` ;

CREATE TABLE IF NOT EXISTS `OFF`.`store` (
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`name`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OFF`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OFF`.`user` ;

CREATE TABLE IF NOT EXISTS `OFF`.`user` (
  `email_address` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`email_address`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OFF`.`products_users_relation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OFF`.`products_users_relation` ;

CREATE TABLE IF NOT EXISTS `OFF`.`products_users_relation` (
  `good_product_link` VARCHAR(256) NOT NULL,
  `user_email_address` VARCHAR(45) NOT NULL,
  `bad_product_link` VARCHAR(256) NOT NULL,
  PRIMARY KEY (`good_product_link`, `user_email_address`, `bad_product_link`),
  INDEX `fk_product_has_user_user1_idx` (`user_email_address` ASC) VISIBLE,
  INDEX `fk_product_has_user_product1_idx` (`good_product_link` ASC) VISIBLE,
  CONSTRAINT `fk_product_has_user_product1`
    FOREIGN KEY (`good_product_link`)
    REFERENCES `OFF`.`product` (`link`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_has_user_user1`
    FOREIGN KEY (`user_email_address`)
    REFERENCES `OFF`.`user` (`email_address`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OFF`.`product_store_relation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OFF`.`product_store_relation` ;

CREATE TABLE IF NOT EXISTS `OFF`.`product_store_relation` (
  `product_link` VARCHAR(256) NOT NULL,
  `store_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`product_link`, `store_name`),
  INDEX `fk_product_has_store_store1_idx` (`store_name` ASC) VISIBLE,
  INDEX `fk_product_has_store_product1_idx` (`product_link` ASC) VISIBLE,
  CONSTRAINT `fk_product_has_store_product1`
    FOREIGN KEY (`product_link`)
    REFERENCES `OFF`.`product` (`link`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_has_store_store1`
    FOREIGN KEY (`store_name`)
    REFERENCES `OFF`.`store` (`name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
