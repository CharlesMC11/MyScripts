//
// Charles Mesa Cayobit
//

#include "move_file.hh"
#include <filesystem>

namespace cmc {

    // move_file

    void move_file(const std::filesystem::path& file,
                   const std::filesystem::path& target_dir)
    {
        std::filesystem::rename(file, target_dir / file.filename());
    }

    // move_image

    void move_image(const std::filesystem::path& image_file,
                    const std::filesystem::path& target_dir)
    {
        move_file(image_file, target_dir);

        const auto& sidecar_file{const_cast<std::filesystem::path&>(image_file)
                                         .replace_extension("xmp")};
        try {
            move_file(sidecar_file, target_dir);
        }
        catch (const std::filesystem::filesystem_error&) {
            // Do nothing if a sidecar file does not exist.
        }
    }

} // namespace cmc