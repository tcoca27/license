const localhost = 'http://localhost:8080';
const ip = 'http://192.168.1.10:8080';
const baseUrl = localhost;

export const ENDPOINT = {
  AUTH_API: {
    SIGNIN: baseUrl + '/api/auth/signin',
    SIGNUP: baseUrl + '/api/auth/signup',
  },
  USER_API: {
    USER: (username: string) => {
      return baseUrl + `/api/user/${username}`;
    },
  },
  VIDEOS_API: {
    UPLOAD_ONE: baseUrl + '/api/videos/uploadVideo',
    UPLOAD_MULTIPLE: baseUrl + '/api/videos/uploadVideos',
    GET_VIDEOS: baseUrl + '/api/videos/',
    MY: baseUrl + '/api/videos/my',
    GET_ONE: (id: number) => {
      return baseUrl + `/api/videos/info/${id}`;
    },
    STREAM: (id: number) => {
      return baseUrl + `/api/videos/${id}`;
    },
    RESULTS: (id: number) => {
      return baseUrl + `/api/videos/results/${id}`;
    },
    PAINT: (id: number) => {
      return baseUrl + `/api/videos/${id}/paint`;
    },
    PERSONS: (id: number) => {
      return baseUrl + `/api/videos/${id}/persons`;
    },
    SIDE: (id: number) => {
      return baseUrl + `/api/videos/${id}/side`;
    }
  }
};
