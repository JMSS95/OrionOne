<?php

namespace App\Http\Controllers;

/**
 * @OA\Info(
 *     version="1.0.0",
 *     title="OrionOne API",
 *     description="IT Service Management System - API Documentation",
 *     @OA\Contact(
 *         email="support@orionone.pt"
 *     )
 * )
 *
 * @OA\Server(
 *     url="http://localhost:8888/api",
 *     description="Development Server"
 * )
 *
 * @OA\SecurityScheme(
 *     securityScheme="sanctum",
 *     type="http",
 *     scheme="bearer",
 *     bearerFormat="JWT",
 *     description="Enter token in format: Bearer {token}"
 * )
 */
abstract class Controller
{
    //
}
