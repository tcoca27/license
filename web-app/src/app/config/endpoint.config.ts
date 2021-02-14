export const ENDPOINT = {
  AUTH_API: {
    SIGNIN: 'http://localhost:8080/api/auth/signin',
    SIGNUP: 'http://localhost:8080/api/auth/signup',
  },
  TESP_API: {
    USER: 'http://localhost:8080/api/test/user',
    ADMIN: 'http://localhost:8080/api/test/admin',
    ALL: 'http://localhost:8080/api/test/all'
  },
  VIDEOS_API: {
    UPLOAD_ONE: 'http://localhost:8080/api/videos/uploadVideo',
    UPLOAD_MULTIPLE: 'http://localhost:8080/api/videos/uploadVideos',
    GET_VIDEOS: 'http://localhost:8080/api/videos/getAll',
    GET_ONE: (id: number) => {
      return `http://localhost:8080/api/videos/info/${id}`;
    },
    STREAM: (id: number) => {
      return `http://localhost:8080/api/videos/${id}`;
    },
  }
};
