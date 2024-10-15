<script>
	import { page } from '$app/stores';
</script>

<div class="root">
	<h1>{$page.error?.message}</h1>
</div>

<style>
	.root {
		position: fixed;
		display: flex;
		justify-content: center;
		top: 0px;
		left: 0px;
		width: 100vw;
		height: 100vh;
		text-align: center;
		align-items: center;
		z-index: -1;
	}
</style>
