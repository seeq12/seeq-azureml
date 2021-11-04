<template>
  <v-menu
      offset-y
      left
  >
    <template v-slot:activator="{ on, attrs }">
      <v-app-bar-nav-icon
          v-bind="attrs"
          v-on="on"
      >
      </v-app-bar-nav-icon>
    </template>
    <v-list>
      <v-divider></v-divider>
      <v-list-item
          value="help"
          href='mailto: applied.research@seeq.com?subject=AzureML Add-on Feedback'
          ripple
      >
        <v-list-item-action class="mr-2 ml-0">
          <v-icon
              color="#212529"
          >
            fa-life-ring
          </v-icon>
        </v-list-item-action>
        <v-list-item-action-text>
          Send Support Request
        </v-list-item-action-text>
      </v-list-item>
      <v-divider></v-divider>
    </v-list>
  </v-menu>
</template>