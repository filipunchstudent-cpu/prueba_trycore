<script setup>
import { onMounted, reactive, ref } from 'vue'

import {
  createActivity,
  createProject,
  deleteActivity,
  deleteProject,
  getProjects,
  updateActivity,
} from './api'

const projects = ref([])
const loading = ref(true)
const savingProject = ref(false)
const savingActivity = ref(false)
const deletingId = ref('')
const error = ref('')
const editingActivityId = ref(null)

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

function resetActivityForm() {
  editingActivityId.value = null
  activityForm.name = ''
  activityForm.bac = ''
  activityForm.planned_percent = ''
  activityForm.actual_percent = ''
  activityForm.ac = ''
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

  const payload = {
    name: activityForm.name.trim(),
    bac: activityForm.bac,
    planned_percent: activityForm.planned_percent,
    actual_percent: activityForm.actual_percent,
    ac: activityForm.ac,
  }

  try {
    if (editingActivityId.value) {
      await updateActivity(activityForm.projectId, editingActivityId.value, payload)
    } else {
      await createActivity(activityForm.projectId, payload)
    }

    resetActivityForm()
    await loadProjects()
  } catch {
    error.value = 'No pude guardar la actividad. Revisa los datos ingresados.'
  } finally {
    savingActivity.value = false
  }
}

function startEditActivity(projectId, activity) {
  editingActivityId.value = activity.id
  activityForm.projectId = String(projectId)
  activityForm.name = activity.name
  activityForm.bac = activity.bac
  activityForm.planned_percent = activity.planned_percent
  activityForm.actual_percent = activity.actual_percent
  activityForm.ac = activity.ac
}

async function removeActivity(projectId, activityId) {
  deletingId.value = `activity-${activityId}`
  error.value = ''

  try {
    await deleteActivity(projectId, activityId)
    await loadProjects()
  } catch {
    error.value = 'No pude eliminar la actividad.'
  } finally {
    deletingId.value = ''
  }
}

async function removeProject(projectId) {
  deletingId.value = `project-${projectId}`
  error.value = ''

  try {
    await deleteProject(projectId)
    await loadProjects()
  } catch {
    error.value = 'No pude eliminar el proyecto.'
  } finally {
    deletingId.value = ''
  }
}

function metricNumber(value) {
  if (value === null || value === undefined) {
    return 0
  }

  return Number(value)
}

function chartRows(project) {
  const rows = [
    { label: 'PV', value: metricNumber(project.metrics.pv), className: 'pv' },
    { label: 'EV', value: metricNumber(project.metrics.ev), className: 'ev' },
    { label: 'AC', value: metricNumber(project.metrics.ac), className: 'ac' },
  ]

  const max = Math.max(...rows.map((row) => row.value), 1)

  return rows.map((row) => ({
    ...row,
    width: `${Math.max((row.value / max) * 100, 2)}%`,
  }))
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
        <h2>{{ editingActivityId ? 'Editar actividad' : 'Nueva actividad' }}</h2>

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

        <div class="actions">
          <button type="submit" :disabled="savingActivity">
            {{ savingActivity ? 'Guardando...' : editingActivityId ? 'Actualizar actividad' : 'Crear actividad' }}
          </button>

          <button
            v-if="editingActivityId"
            class="secondary"
            type="button"
            @click="resetActivityForm"
          >
            Cancelar edición
          </button>
        </div>
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

          <div class="actions">
            <span class="status" :class="project.metrics.cost_status">
              {{ project.metrics.cost_status }}
            </span>

            <button
              class="danger"
              type="button"
              :disabled="deletingId === `project-${project.id}`"
              @click="removeProject(project.id)"
            >
              Eliminar
            </button>
          </div>
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

        <div class="metrics"> </div>

        <div class="chart" aria-label="Comparación PV EV AC">
          <div
            v-for="row in chartRows(project)"
            :key="row.label"
            class="chart-row"
          >
            <span>{{ row.label }}</span>

            <div class="chart-track">
              <div
                class="chart-bar"
                :class="row.className"
                :style="{ width: row.width }"
              >
                {{ row.value.toLocaleString('es-CO') }}
              </div>
            </div>
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
              <th>Acciones</th>
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
              <td>
                <div class="table-actions">
                  <button
                    class="secondary"
                    type="button"
                    @click="startEditActivity(project.id, activity)"
                  >
                    Editar
                  </button>

                  <button
                    class="danger"
                    type="button"
                    :disabled="deletingId === `activity-${activity.id}`"
                    @click="removeActivity(project.id, activity.id)"
                  >
                    Eliminar
                  </button>
                </div>
              </td>
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