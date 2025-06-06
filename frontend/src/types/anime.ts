export enum AnimeStatus {
  WATCHED = "watched",
  PLANNED = "planned",
  COMPLETED = "completed"
}

export interface AnimeCreate {
  mal_id: number;
  title: string;
  thumbnail: string;
  total_episodes: number;
  status: AnimeStatus;
  user_score?: number | null;
  user_review?: string | null;
  complete_episodes?: number;
}

export interface AnimeUpdate {
  status?: AnimeStatus;
  user_score?: number | null;
  user_review?: string | null;
  complete_episodes?: number;
}

export interface AnimeResponse extends AnimeCreate {
  id: number;
} 