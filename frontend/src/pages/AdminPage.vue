<template>
  <q-page
    class="window-height window-width row justify-center items-center"
    style="background: #111827"
  >
    <div class="column items-center">
      <div class="text-h4 text-white text-bold q-mb-md">Bem Vindo(a)!</div>
      <div class="text-subtitle1 text-blue-grey-2 q-mb-xl" style="opacity: 0.5">
        Selecione a página desejada
      </div>

      <div class="row q-gutter-md">
        <q-card
          flat
          class="my-card column items-center justify-center cursor-pointer"
          style="
            background: #1f2937;
            border: 1px solid #30363d;
            width: 12dvw;
            height: 12dvw;
            border-radius: 20px;
          "
          @click="selectRoom('Solicitações')"
        >
          <q-card-section class="column items-center">
            <q-icon name="computer" size="3.5vw" color="green-4" />
            <div class="text-h6 text-white q-mt-md">Solicitações</div>
          </q-card-section>
        </q-card>
        <q-card
          flat
          class="my-card column items-center justify-center cursor-pointer"
          style="
            background: #1f2937;
            border: 1px solid #30363d;
            width: 12dvw;
            height: 12dvw;
            border-radius: 20px;
          "
          @click="selectRoom('Registrar nova Sala')"
        >
          <q-card-section class="column items-center">
            <q-icon name="school" size="3.5vw" color="blue-4" />
            <div class="text-h6 text-white q-mt-md">Registrar nova Sala</div>
          </q-card-section>
        </q-card>
        <q-card
          flat
          class="my-card column items-center justify-center cursor-pointer"
          style="
            background: #1f2937;
            border: 1px solid #30363d;
            width: 12dvw;
            height: 12dvw;
            border-radius: 20px;
          "
          @click="selectRoom('Painel Admin')"
        >
          <q-card-section class="column items-center">
            <q-icon name="science" size="3.5vw" color="yellow-4" />
            <div class="text-h6 text-white q-mt-md">Painel Admin</div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { Dialog } from 'quasar';
import AvailableRoomsComponent from '../components/AvailableRoomsComponent.vue';

function selectRoom(roomType) {
  console.log('Tipo de ambiente selecionado:', roomType);

  Dialog.create({
    component: AvailableRoomsComponent,

    componentProps: {
      roomType: roomType,
    },
  })
    .onOk(() => {
      console.log('OK');
    })
    .onCancel(() => {
      console.log('Cancel');
    })
    .onDismiss(() => {
      console.log('Called on OK or Cancel');
    });
}
</script>
