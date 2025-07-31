//
// Charles Mesa Cayobit
//

#include "read_targets_file.hh"
#include <filesystem>
#include <fstream>
#include <regex>
#include <string>

namespace cmc {

    auto read_targets_file(const std::filesystem::path& targets_file)
            -> std::pair<Directories, Targets>
    {
        std::ifstream file{targets_file};

        Directories dirs;
        Targets targets;

        std::string line;
        const std::regex pattern{
                R"(^\s*?(\w+?)\s*?=\s*?(\w+?[\/|\\]?\w+?)\s*?$)"};
        std::smatch match;

        while (std::getline(file, line)) {
            if (line.empty() || line.starts_with('#')) { continue; }

            std::regex_search(line, match, pattern);
            if (match.size() < 3) { continue; }

            const auto key{match[1].str()};
            const std::filesystem::path value{match[2].str()};

            dirs.insert(value);
            targets[key] = value;
        }
        dirs.insert(MISC_DIR);

        return {dirs, targets};
    }

} // namespace cmc