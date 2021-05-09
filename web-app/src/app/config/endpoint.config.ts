const localhost = 'http://localhost:8080';
const ip = 'http://192.168.1.10:8080';
const baseUrl = localhost;

export const ENDPOINT = {
  AUTH_API: {
    SIGNIN: baseUrl + '/api/auth/signin',
    SIGNUP: baseUrl + '/api/auth/signup',
  },
  TESP_API: {
    USER: baseUrl + '/api/test/user',
    ADMIN: baseUrl + '/api/test/admin',
    ALL: baseUrl + '/api/test/all'
  },
  VIDEOS_API: {
    UPLOAD_ONE: baseUrl + '/api/videos/uploadVideo',
    UPLOAD_MULTIPLE: baseUrl + '/api/videos/uploadVideos',
    GET_VIDEOS: baseUrl + '/api/videos/',
    GET_ONE: (id: number) => {
      return baseUrl + `/api/videos/info/${id}`;
    },
    STREAM: (id: number) => {
      return baseUrl + `/api/videos/${id}`;
    },
  }
};
