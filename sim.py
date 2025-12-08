from common import get_soup_from_file

SCHOOL_OPTIONS_FILENAME = "sim_school_options.html"

class SimUtils:
    @staticmethod
    def get_sim_school_to_id_map() -> dict[str, str]:
        soup = get_soup_from_file(SCHOOL_OPTIONS_FILENAME)

        data_map = {}
        for option in soup.find_all("option"):
            if option.has_attr("value"):
                data_map[option.text] = option["value"]
        
        return data_map
