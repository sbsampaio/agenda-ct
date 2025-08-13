<template>
  <q-page
    class="window-height window-width row justify-center items-center"
    style="background: #111827"
  >
    <div class="column items-center">
      <div class="text-h4 text-white q-mb-md">Portal de Agendamentos do CT</div>
      <q-card
        bordered
        class="q-pa-lg shadow-24"
        style="background: #1f2937; border: 1px solid #30363d; border-radius: 20px"
      >
        <q-card-section>
          <div class="row justify-center">
            <q-avatar
              size="xl"
              font-size="52px"
              icon="account_circle"
              style="color: #3b82f6"
            ></q-avatar>
          </div>
          <div class="text-subtitle1 text-center text-blue-grey-2 q-mt-md" style="opacity: 0.5">
            Faça login para continuar
          </div>
        </q-card-section>

        <q-card-section>
          <q-form class="q-gutter-md">
            <q-input
              filled
              clearable
              v-model="email"
              type="email"
              label="exemplo@email.com"
              style="
                background: #111827;
                border: 1px solid #30363d;
                border-radius: 5px;
                width: 20dvw;
              "
              dark
              input-class="text-blue-grey-2"
              label-color="blue-grey-4"
            >
              <template v-slot:prepend>
                <q-icon name="email" color="blue-grey-4" />
              </template>
            </q-input>

            <q-input
              filled
              clearable
              v-model="password"
              type="password"
              label="************"
              style="
                background: #111827;
                border: 1px solid #30363d;
                border-radius: 5px;
                width: 20dvw;
              "
              dark
              input-class="text-blue-grey-2"
              label-color="blue-grey-4"
            >
              <template v-slot:prepend>
                <q-icon name="lock" color="blue-grey-4" />
              </template>
            </q-input>
          </q-form>
        </q-card-section>

        <q-card-actions class="q-px-lg">
          <q-btn
            unelevated
            size="lg"
            color="primary"
            class="full-width text-white"
            label="Entrar"
            @click="login"
            style="border-radius: 5px"
          />
        </q-card-actions>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { ref } from 'vue';
import { Notify } from 'quasar';

const email = ref('');
const password = ref('');

function login() {
  console.log('Email:', email.value);
  console.log('Password:', password.value);

  Notify.create({
    color: 'positive',
    message: 'Login realizado com sucesso!',
  });
}
</script>
