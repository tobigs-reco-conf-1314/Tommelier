import axios from "axios";

const WINE_API_URL = "http://35.200.102.226"
const RECO_API_URL = "http://49.50.160.197:8000"

export type RecoDTO = {
  mood: string;
  food: string;
  sweet: number;
  tannin: number;
  body: number;
  acidity: number;
};

export type WineDTO = {
  id: number;
  name: string;
  rating_count: number;
  rating_average: number;
  rating_distribution: number[];
  wine_type: number;
  alcohol: number;
  acidity: number;
  body: number;
  intensity: number;
  sweetness: number | null;
  tannin: number | null;
  grapes: string[];
  grapes_id: number[];
  foods: string[];
  region_id: number;
  region: string;
  country_code: string;
  rank_global: number;
  rank_global_total: number;
  rank_country: number;
  rank_country_total: number;
  rank_region: number;
  rank_region_total: number;
  rank_winery: number;
  rank_winery_total: number;
  img_url: string;
};

const api = {
  getMultiWineInfos: async (recommendations: number[]) => {
    const result = await axios.post<WineDTO[]>(
      `${WINE_API_URL}/api/wines/multi/`,
      recommendations
    );
    return result.data;
  },

  getRecommendation: async (body: RecoDTO) => {
    const result = await axios.post<Record<string, number[]>>(
      `${RECO_API_URL}/reco/`,
      body
    );
    return result.data.wine_ids;
  },
};

export default api;
