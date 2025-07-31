//
// Charles Mesa Cayobit
//

#ifndef ORGANIZE_DIRECTORY_CONTENTS_READ_TARGETS_FILE_HH
#define ORGANIZE_DIRECTORY_CONTENTS_READ_TARGETS_FILE_HH

#include <filesystem>
#include <unordered_map>
#include <unordered_set>
#include <utility>

using namespace std::string_literals;

namespace cmc {

    using Directories = std::unordered_set<std::filesystem::path>;
    using Targets = std::unordered_map<std::string, std::filesystem::path>;

    static const std::filesystem::path MISC_DIR{"Misc"s};

    /// \brief Create a targets map from a file.
    /// \param targets_file the file containing the mapping corresponding file's
    /// destination
    auto read_targets_file(const std::filesystem::path& targets_file)
            -> std::pair<Directories, Targets>;

} // namespace cmc

#endif // ORGANIZE_DIRECTORY_CONTENTS_READ_TARGETS_FILE_HH