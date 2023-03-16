# A P-dimensional region where P is the number of indicators
import random


class TemplatingEngine:
    def __init__(self):
        self.regions = self.load_regions()  # [(diag_endpoint_1, diag_endpoint_2)...]
        self.templates = self.load_templates()  # {Region_index  -> {Hook String: Probability Mass}}

    # TODO: Add regions
    def load_regions(self):
        return []

    # TODO: Add templates
    def load_templates(self):
        return {}

    def find_region(self, indicator_vector):
        """
        Finds the region a given point belongs to in an N-dimensional space.

        Returns:
        int: The index of the region the point belongs to, or -1 if the point does not belong to any region.
        """
        for i, region in enumerate(self.regions):
            lower_bounds, upper_bounds = region
            if all(lower_bound <= coord <= upper_bound for lower_bound, upper_bound, coord in
                   zip(lower_bounds, upper_bounds, indicator_vector)):
                return i
        return -1

    def fetch_template(self, region_index):
        probability_distribution = self.templates[region_index]
        return random.choices(probability_distribution.keys(), weights=probability_distribution.values())[0]
