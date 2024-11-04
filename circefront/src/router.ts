import { html } from 'lit';

if (!(globalThis as any).URLPattern) {
  await import("urlpattern-polyfill");
}

import { Router } from '@thepassle/app-tools/router.js';
import { lazy } from '@thepassle/app-tools/router/plugins/lazy.js';
// @ts-ignore
import { title } from '@thepassle/app-tools/router/plugins/title.js';

import './pages/app-home.js';

const baseURL: string = (import.meta as any).env.BASE_URL;

export const router = new Router({
  routes: [
    {
      path: resolveRouterPath(), // Home Route
      title: 'Home',
      render: () => html`<app-home></app-home>`
    },
    {
      path: resolveRouterPath('group/:id'), // Dynamic Group Route
      title: 'Group',
      plugins: [
        lazy(() => import('./pages/attendance-list.js')), // Lazy load the attendance-list page
      ],
      render: (context) => {
        const groupId = context.params.id; // Extract groupId from the route
            console.log('Group ID from route:', groupId); // Ensure the groupId is logged and not empty

        return html`<classes-list groupId="${groupId}"></classes-list>`; // Pass groupId to the classes-list component
      }
    },
    {
      path: resolveRouterPath('groups'), // About Route
      title: 'Groups',
      plugins: [
        lazy(() => import('./pages/classes-list.js')), // Lazy load the about page
      ],
      render: () => html`<new-page></new-page>`
    }
  ]
});

// Function to resolve a path using the BASE_URL from the environment
export function resolveRouterPath(unresolvedPath?: string) {
  let resolvedPath = baseURL;
  if (unresolvedPath) {
    resolvedPath = resolvedPath + unresolvedPath;
  }
  return resolvedPath;
}
