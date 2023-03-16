<template>
    <div class='main-cont'>
        <div class='body-cont'>
            <NavbarDefault />
            <Nuxt />
        </div>
    </div>
</template>

<script>
import NavbarDefault from '@/components/navbar/NavbarDefault.vue'

export default {
    name: 'default',
    components: {
        NavbarDefault
    }
}
</script>