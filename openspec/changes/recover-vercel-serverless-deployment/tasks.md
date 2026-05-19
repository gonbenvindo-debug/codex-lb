## 1. Vercel entrypoint and routing

- [ ] 1.1 Replace the lightweight Vercel health shim with the real FastAPI application entrypoint
- [ ] 1.2 Rebuild `vercel.json` so API and health prefixes route to the Python Function and SPA routes fall back to `index.html`
- [ ] 1.3 Remove root-level Python source exposure from the deployment surface

## 2. Frontend build output

- [ ] 2.1 Make the Vite build output configurable so Docker/local still target `app/static`
- [ ] 2.2 Add a Vercel build script that emits the SPA to `public/`
- [ ] 2.3 Pin the Vercel Python runtime to the supported 3.13 line

## 3. Serverless runtime behavior

- [ ] 3.1 Add explicit serverless defaults that reduce connection pressure and force HTTP/SSE-safe upstream behavior
- [ ] 3.2 Skip long-lived schedulers, bridge registration, metrics, and cache polling in serverless mode
- [ ] 3.3 Add protected internal cron endpoints that run one-shot maintenance tasks

## 4. Verification

- [ ] 4.1 Add regression tests for serverless settings and cron endpoint authorization
- [ ] 4.2 Run focused local tests that do not require unavailable external services
- [ ] 4.3 Validate the Vercel deployment shape with a fresh deployment
