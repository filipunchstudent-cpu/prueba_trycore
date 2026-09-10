<script setup>
import { onMounted, reactive, ref } from 'vue'

import { createActivity, createProject, getProjects } from './api'

const projects = ref([])
const loading = ref(true)
const savingProject = ref(false)
const savingActivity = ref(false)
const error = ref('')

const projectForm = reactive({
  name: '',
})

const activityForm = reactive({
  projectId: '',
  name: '',
  bac: '',
  planned_percent: '',
  actual_percent: '',
  ac: '',
})

async function loadProjects() {
  loading.value = true
  error.value = ''

  try {
    projects.value = await getProjects()

    if (!activityForm.projectId && projects.value.length > 0) {
      activityForm.projectId = String(projects.value[0].id)
    }
  } catch {
    error.value = 'No pude cargar los proyectos. Revisa que el backend esté encendido.'
  } finally {
    loading.value = false
  }
}

async function submitProject() {
  if (!projectForm.name.trim()) {
    error.value = 'El nombre del proyecto es obligatorio.'
    return
  }

  savingProject.value = true
  error.value = ''

  try {
    const created = await createProject({
      name: projectForm.name.trim(),
    })

    projectForm.name = ''
    activityForm.projectId = String(created.id)
    await loadProjects()
  } catch {
    error.value = 'No pude crear el proyecto.'
  } finally {
    savingProject.value = false
  }
}

async function submitActivity() {
  if (!activityForm.projectId) {
    error.value = 'Primero crea o selecciona un proyecto.'
    return
  }

  savingActivity.value = true
  error.value = ''

  try {
    await createActivity(activityForm.projectId, {
      name: activityForm.name.trim(),
      bac: activityForm.bac,
      planned_percent: activityForm.planned_percent,
      actual_percent: activityForm.actual_percent,
      ac: activityForm.ac,
    })

    activityForm.name = ''
    activityForm.bac = ''
    activityForm.planned_percent = ''
    activityForm.actual_percent = ''
    activityForm.ac = ''

    await loadProjects()
  } catch {
    error.value = 'No pude crear la actividad. Revisa los datos ingresados.'
  } finally {
    savingActivity.value = false
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

    <section class="forms">
      <form class="panel" @submit.prevent="submitProject">
        <h2>Nuevo proyecto</h2>

        <label>
          Nombre
          <input v-model="projectForm.name" type="text" placeholder="Proyecto demo EVM" />
        </label>

        <button type="submit" :disabled="savingProject">
          {{ savingProject ? 'Guardando...' : 'Crear proyecto' }}
        </button>
      </form>

      <form class="panel" @submit.prevent="submitActivity">
        <h2>Nueva actividad</h2>

        <label>
          Proyecto
          <select v-model="activityForm.projectId">
            <option value="">Selecciona un proyecto</option>
            <option v-for="project in projects" :key="project.id" :value="String(project.id)">
              {{ project.name }}
            </option>
          </select>
        </label>

        <label>
          Nombre
          <input v-model="activityForm.name" type="text" placeholder="Desarrollo" />
        </label>

        <div class="field-grid">
          <label>
            BAC
            <input v-model="activityForm.bac" type="number" min="0" step="0.01" />
          </label>

          <label>
            Planeado %
            <input v-model="activityForm.planned_percent" type="number" min="0" max="100" step="0.01" />
          </label>

          <label>
            Real %
            <input v-model="activityForm.actual_percent" type="number" min="0" max="100" step="0.01" />
          </label>

          <label>
            AC
            <input v-model="activityForm.ac" type="number" min="0" step="0.01" />
          </label>
        </div>

        <button type="submit" :disabled="savingActivity">
          {{ savingActivity ? 'Guardando...' : 'Crear actividad' }}
        </button>
      </form>
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