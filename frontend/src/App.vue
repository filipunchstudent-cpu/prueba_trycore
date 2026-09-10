<script setup>
import { onMounted, ref } from 'vue'

import { getProjects } from './api'

const projects = ref([])
const loading = ref(true)
const error = ref('')

async function loadProjects() {
  loading.value = true
  error.value = ''

  try {
    projects.value = await getProjects()
  } catch {
    error.value = 'No pude cargar los proyectos. Revisa que el backend esté encendido.'
  } finally {
    loading.value = false
  }
}

onMounted(loadProjects)
</script>

<template>
  <main class="page">
    <section class="header">
      <div>
        <p class="eyebrow">Gestión de Valor Ganado</p>
        <h1>Dashboard EVM</h1>
      </div>

      <button type="button" @click="loadProjects">Actualizar</button>
    </section>

    <p v-if="loading" class="message">Cargando proyectos...</p>
    <p v-else-if="error" class="message error">{{ error }}</p>

    <section v-else class="project-list">
      <article v-for="project in projects" :key="project.id" class="project">
        <div class="project-header">
          <div>
            <h2>{{ project.name }}</h2>
            <p>{{ project.activities.length }} actividades</p>
          </div>

          <span class="status" :class="project.metrics.cost_status">
            {{ project.metrics.cost_status }}
          </span>
        </div>

        <div class="metrics">
          <div>
            <span>BAC</span>
            <strong>{{ project.metrics.bac }}</strong>
          </div>
          <div>
            <span>PV</span>
            <strong>{{ project.metrics.pv }}</strong>
          </div>
          <div>
            <span>EV</span>
            <strong>{{ project.metrics.ev }}</strong>
          </div>
          <div>
            <span>AC</span>
            <strong>{{ project.metrics.ac }}</strong>
          </div>
          <div>
            <span>CPI</span>
            <strong>{{ project.metrics.cpi || 'N/A' }}</strong>
          </div>
          <div>
            <span>SPI</span>
            <strong>{{ project.metrics.spi || 'N/A' }}</strong>
          </div>
        </div>

        <table>
          <thead>
            <tr>
              <th>Actividad</th>
              <th>BAC</th>
              <th>Planeado %</th>
              <th>Real %</th>
              <th>AC</th>
              <th>EV</th>
              <th>PV</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="activity in project.activities" :key="activity.id">
              <td>{{ activity.name }}</td>
              <td>{{ activity.bac }}</td>
              <td>{{ activity.planned_percent }}</td>
              <td>{{ activity.actual_percent }}</td>
              <td>{{ activity.ac }}</td>
              <td>{{ activity.metrics.ev }}</td>
              <td>{{ activity.metrics.pv }}</td>
            </tr>
          </tbody>
        </table>
      </article>

      <p v-if="projects.length === 0" class="message">
        No hay proyectos todavía.
      </p>
    </section>
  </main>
</template>