# Dummy Flask App Design

## Intent

Create a small, attractive Flask app that is easy to run locally and deploy as a demonstration project.

## Goals

- Serve a polished, responsive home page at `/`.
- Keep the application stateless and database-free.
- Include a smoke test and concise setup instructions.

## Non-goals

- Authentication, forms, APIs, persistence, or JavaScript frameworks.
- Multiple pages or configurable themes.

## Constraints

- Flask and server-rendered Jinja HTML.
- Plain CSS with no external asset or CDN dependency.
- A production-compatible WSGI entry point.

## Approach

Use a conventional small Flask layout: an application module, one Jinja template, and one stylesheet. A single-file inline-template alternative was rejected because it makes visual maintenance awkward; a frontend framework was rejected as unnecessary for a static landing page.

