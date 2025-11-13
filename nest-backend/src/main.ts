import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
    const app = await NestFactory.create(AppModule);

    // Enable CORS
    app.enableCors({
        origin: process.env.FRONTEND_URL || 'http://localhost:3000',
        credentials: true,
    });

    // Global prefix for all routes
    app.setGlobalPrefix('api');

    const port = process.env.PORT ?? 3001;
    await app.listen(port);
    console.log(`🚀 Backend running on http://localhost:${port}/api`);
}
bootstrap();
