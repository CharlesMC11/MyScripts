//
// Charles Mesa Cayobit
// A CLI program to organize the contents of a directory.
//

#include "move_file.hh"
#include "read_targets_file.hh"
#include <filesystem>
#include <iostream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>

void show_usage(std::string_view);

/// \todo Maybe a better way of handling CLI args?
int main(const int argc, const char* argv[])
{
    if (argc < 2) {
        show_usage(argv[0]);
        return EXIT_FAILURE;
    }
    const std::filesystem::path root_dir{argv[1]};

    std::filesystem::path targets_file;
    if (argc < 3) { targets_file = root_dir / "targets.cfg"; }
    else {
        targets_file = argv[2];
    }

    auto [subdirs, target_dirs]{cmc::read_targets_file(targets_file)};

    for (const auto& subdir: subdirs) {
        std::filesystem::create_directories(root_dir / subdir);
    }

    // `move_image()` will move an image's existing sidecar file
    // alongside the image, so defer processing XMP files to the
    // end.
    std::vector<std::filesystem::path> xmp_files;

    // Ensures that if the targets file is in the same directory as
    // the root, it will be skipped
    subdirs.insert(targets_file.filename());

    const auto& images_dir{target_dirs["jpg"s]};
    const auto& images_raw_dir{target_dirs["dng"s]};
    for (const auto& dir: std::filesystem::directory_iterator{root_dir}) {
        const auto& dir_path{dir.path()};

        if (subdirs.contains(dir_path.filename())
            || dir_path.filename().string() == ".DS_Store"s) {
            continue;
        }

        auto file_ext{dir_path.extension().string()};
        std::filesystem::path target_dir;
        if (file_ext.empty()) { target_dir = cmc::MISC_DIR; }
        else {
            file_ext = file_ext.substr(1);
            for (auto& c: file_ext) { c = static_cast<char>(std::tolower(c)); }

            if (file_ext == "xmp") {
                xmp_files.push_back(dir_path);
                continue;
            }

            try {
                target_dir = target_dirs.at(file_ext);
            }
            catch (const std::out_of_range&) {
                target_dir = cmc::MISC_DIR;
            }
        }

        if (target_dir == images_dir || target_dir == images_raw_dir) {
            cmc::move_image(dir_path, root_dir / target_dir);
        }
        else {
            cmc::move_file(dir_path, root_dir / target_dir);
        }
    }

    for (const auto& xmp_file: xmp_files) {
        try {
            cmc::move_file(xmp_file, root_dir / cmc::MISC_DIR);
        }
        catch (const std::filesystem::filesystem_error&) {
            // Do nothing if the image sidecar file had already been
            // moved.
        }
    }
}

// implementation details below

void show_usage(std::string_view program_name)
{
    std::cerr << "usage: " << program_name
              << " [-v | --verbose, -h | --help] directory "
                 "targets_file\n";
}