from algorithms.color_refinement import color_refinement, fast_color_refinement

class Default_color_refinement:
    """
    Maps self.color_refine(G: "Graph") to algorithms.color_refinement(G: "Graph").
    """
    def color_refine(self, G: "Graph"):
        return color_refinement(G)

class Fast_color_refinement:
    """
    Maps self.color_refine(G: "Graph") to algorithms.fast_color_refinement(G: "Graph").
    """
    def color_refine(self, G: "Graph"):
        return fast_color_refinement(G)