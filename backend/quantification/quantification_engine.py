from typing import Dict, Any

class ConstructionQuantificationEngine:
    """
    Calculates material quantities and surface areas from 3D building measurements.
    """
    @staticmethod
    def calculate_quantities(
        total_area: float, 
        building_height: float, 
        floor_count: int,
        wall_area: float = None
    ) -> Dict[str, Any]:
        area = max(total_area, 1.0)
        floors = max(floor_count, 1)
        height = max(building_height, 3.0)

        # Standard engineering estimation formulas
        concrete_volume_m3 = round(area * 0.25 * floors, 2)
        steel_rebar_tons = round(concrete_volume_m3 * 0.08, 2) # ~80kg per m3
        cement_bags = int(concrete_volume_m3 * 7.5) # ~7.5 bags per m3 M20/M25
        sand_tons = round(concrete_volume_m3 * 0.45, 2)
        aggregate_tons = round(concrete_volume_m3 * 0.85, 2)

        est_wall_area = wall_area if wall_area and wall_area > 0 else round(area * 2.8 * floors, 2)
        paint_area_sqm = round(est_wall_area + (area * floors), 2)
        tile_area_sqm = round(area * floors * 0.85, 2) # ~85% carpet area
        plaster_area_sqm = round(est_wall_area * 2, 2) # Internal + external

        return {
            "total_builtup_area_sqm": round(area * floors, 2),
            "concrete_volume_m3": concrete_volume_m3,
            "steel_rebar_tons": steel_rebar_tons,
            "cement_bags": cement_bags,
            "sand_tons": sand_tons,
            "aggregate_tons": aggregate_tons,
            "wall_area_sqm": est_wall_area,
            "paint_area_sqm": paint_area_sqm,
            "tile_area_sqm": tile_area_sqm,
            "plaster_area_sqm": plaster_area_sqm,
        }

quantification_engine = ConstructionQuantificationEngine()
