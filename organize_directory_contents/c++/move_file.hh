//
// Charles Mesa Cayobit
//

#ifndef ORGANIZE_DIRECTORY_CONTENTS_MOVE_FILE_HH
#define ORGANIZE_DIRECTORY_CONTENTS_MOVE_FILE_HH

#include <filesystem>

namespace cmc {

    /// \brief Move `file` into `target_dir`.
    void move_file(const std::filesystem::path& file,
                   const std::filesystem::path& target_dir);

    /// \brief Move an image and its sidecar file to `target_dir`.
    void move_image(const std::filesystem::path& file,
                    const std::filesystem::path& target_dir);

} // namespace cmc

#endif // ORGANIZE_DIRECTORY_CONTENTS_MOVE_FILE_HH