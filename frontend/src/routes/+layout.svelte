<script lang="ts">
	import Navbar from '$lib/components/navbar.svelte';
	import '@fortawesome/fontawesome-free/css/all.min.css';
	export let data;
	import { rootData, errorCode, throwError } from '$lib/stores';
	import Popup from '$lib/components/popup.svelte';
	import Footer from '$lib/components/footer.svelte';
	rootData.set(data);
</script>

{#if $rootData.use_analytics}
	<script
		defer
		src="https://analytics.salanileo.dev/script.js"
		data-website-id="eccefc55-f50f-4c06-9171-c3a68d1f5dfc"
	></script>
{/if}

<div class="layout">
	<div>
		<Navbar {data}></Navbar>
		<slot />
	</div>
	<Footer />
</div>
<Popup bind:message={$throwError} bind:code={$errorCode}></Popup>

<style>
	.layout {
		min-height: 100vh;
		display: flex;
		justify-content: space-between;
		flex-direction: column;
	}
</style>
