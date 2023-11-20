const swaggerJsdoc = require('swagger-jsdoc');

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Your API Documentation',
      version: '1.0.0',
    },
  },
  apis: ['./dist/**/*.js'], // Path to the API routes in your project
};

export const specs = swaggerJsdoc(options);

