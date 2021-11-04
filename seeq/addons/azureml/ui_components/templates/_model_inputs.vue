<template>
  <v-card
      class="ml-5 mr-5 mb-5"
      :style="model_inputs_visible?'background-color:#F6F6F6; opacity: 1; min-width: 300px': 'display: none !important'"
  >
    <v-card-title>
      Model Inputs
    </v-card-title>
    <v-select
        class="ml-5 mr-5"
        style=""
        label="Select the model endpoint"
        dense
        outlined
        filled
        :loading="endpoint_loading"
        loader-height="3"
        :disabled="endpoint_disabled"
        :color="endpoint_color"
        :item-color="endpoint_color"
        :items="endpoint_items"
        v-model="endpoint_selection"
        @change="endpoint_on_change"
    >
    </v-select>
    <v-select
        class="ml-5 mr-5"
        :style="asset_visible?'': 'display: none !important'"
        label="Select asset to apply the model"
        dense
        outlined
        filled
        :disabled="asset_disabled"
        :color="asset_color"
        :item-color="asset_color"
        :items="asset_items"
        v-model="asset_selection"
        @change="asset_on_change"
    >
    </v-select>

  </v-card>
</template>