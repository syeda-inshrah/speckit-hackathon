import { NextResponse } from 'next/server';

/**
 * Health Check Endpoint
 * Used by Docker health checks and Kubernetes liveness probes
 *
 * @returns JSON response with health status
 */
export async function GET() {
  try {
    return NextResponse.json(
      {
        status: 'healthy',
        service: 'todo-frontend',
        version: '1.0.0',
        timestamp: new Date().toISOString(),
      },
      { status: 200 }
    );
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        error: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 503 }
    );
  }
}
