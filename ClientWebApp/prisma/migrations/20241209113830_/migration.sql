/*
  Warnings:

  - Made the column `password` on table `user` required. This step will fail if there are existing NULL values in that column.
  - Made the column `birthday` on table `user` required. This step will fail if there are existing NULL values in that column.
  - Made the column `gender` on table `user` required. This step will fail if there are existing NULL values in that column.

*/
-- AlterTable
ALTER TABLE `user` MODIFY `password` VARCHAR(191) NOT NULL,
    MODIFY `birthday` DATE NOT NULL,
    MODIFY `gender` VARCHAR(191) NOT NULL DEFAULT 'None';
