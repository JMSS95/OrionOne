import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import compression from 'compression';
import helmet from 'helmet';
import { WINSTON_MODULE_NEST_PROVIDER } from 'nest-winston';
import { AppModule } from './app.module';

async function bootstrap() {
    const app = await NestFactory.create(AppModule);

    // Use Winston as the default logger
    app.useLogger(app.get(WINSTON_MODULE_NEST_PROVIDER));

    // Security: Helmet middleware
    app.use(helmet());

    // Performance: Compression middleware
    app.use(compression());

    // Validation: Global validation pipe
    app.useGlobalPipes(
        new ValidationPipe({
            whitelist: true,
            forbidNonWhitelisted: true,
            transform: true,
        }),
    );

    // Enable CORS
    app.enableCors({
        origin: process.env.FRONTEND_URL || 'http://localhost:3000',
        credentials: true,
    });

    // Global prefix for all routes
    app.setGlobalPrefix('api');

    // Swagger/OpenAPI Documentation
    const config = new DocumentBuilder()
        .setTitle('OrionOne ITSM API')
        .setDescription('IT Service Management Platform REST API')
        .setVersion('1.0')
        .addTag('auth', 'Authentication endpoints')
        .addTag('incidents', 'Incident management')
        .addTag('users', 'User management')
        .addTag('knowledge', 'Knowledge base articles')
        .addTag('sla', 'SLA policies')
        .addBearerAuth()
        .build();
    const document = SwaggerModule.createDocument(app, config);
    SwaggerModule.setup('api/docs', app, document);

    const port = process.env.PORT ?? 3001;
    await app.listen(port);

    const logger = app.get(WINSTON_MODULE_NEST_PROVIDER);
    logger.log(
        `Backend running on http://localhost:${port}/api`,
        'Bootstrap',
    );
    logger.log(
        `API Documentation available at http://localhost:${port}/api/docs`,
        'Bootstrap',
    );
}
bootstrap();
