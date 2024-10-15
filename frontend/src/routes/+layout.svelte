<script lang="ts">
	import Navbar from '$lib/components/navbar.svelte';
	import '@fortawesome/fontawesome-free/css/all.min.css';
	export let data;
	import { rootData, errorCode, throwError } from '$lib/stores';
	import Popup from '$lib/components/popup.svelte';
	import { fetch_analytics } from '$lib/get_users_infos.js';
	import { onMount } from 'svelte';
	import Footer from '$lib/components/footer.svelte';
	rootData.set(data);
	// console.log(data);

	let website = data.source;
	let user_ip = data.user_ip;

	onMount(() => {
		if (data.analytics) {
			let userAgent = window.navigator.userAgent;
			fetch_analytics(website, userAgent, user_ip, data.analytics, $rootData.user.info.admin);
		}
	});
</script>

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
