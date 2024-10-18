import os
import shutil


def copy_rename_files(chapter_range, dest_dir):
    chapter_range = [int(x) for x in chapter_range]
    file_count = 1
    for chapter_num in range(chapter_range[0], chapter_range[1] + 1):
        chapter_folder = f"Chapter {chapter_num}"

        if os.path.exists(chapter_folder):
            files = os.listdir(chapter_folder)
            files = sorted(files)

            for file_name in files:
                file_path = os.path.join(chapter_folder, file_name)

                if os.path.isfile(file_path):
                    new_file_name = f"{chapter_num:03}_{file_count:03}{os.path.splitext(file_name)[1]}"
                    dest_file_path = os.path.join(dest_dir, new_file_name)

                    # Copy the file
                    shutil.copy(file_path, dest_file_path)
                    print(f"Copied {file_name} to {dest_file_path}")

                    file_count += 1
        else:
            print(f"Folder '{chapter_folder}' does not exist.")


def convert_to_cbz(dir, destination):
    if os.path.exists(dir):
        folder_name = os.path.basename(dir)

        archive_path = os.path.join(destination, folder_name)
        # Making the zip file
        shutil.make_archive(folder_name, 'zip', dir)
        # Remove Folder
        shutil.rmtree(dir)

        # Change extension
        zip_file_path = archive_path + ".zip"
        cbz_file_path = archive_path + ".cbz"
        os.rename(zip_file_path, cbz_file_path)


try:
    try:
        volumes = int(input("How many Volumes are there <Integer>: ").strip())
    except ValueError:
        print("Insert a valid integer")

    current_volume = 1

    while current_volume <= volumes:
        chapterRange = input(f"Which Chapters belong to Volume {current_volume}: ").strip()
        ranges = [x.strip() for x in chapterRange.split('-')]

        try:
            ranges = [int(x) for x in ranges]
            if len(ranges) != 2 or not ranges[1] >= ranges[0]:
                raise ValueError

        except ValueError:
            print("Use an appropriate format <Number1-Number2> inclusive and Number1 < Number2")
            continue

        current_dir = os.getcwd()
        destination_dir = os.path.join(current_dir, f'Vol.{current_volume}')

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        copy_rename_files(ranges, destination_dir)
        convert_to_cbz(destination_dir, current_dir)
        current_volume += 1

    print("Conversion Complete")

except ValueError as e:
    print("Error: ", e)
