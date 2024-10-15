<script lang="ts">
	export let message: string | undefined = undefined;
	export let code: number | undefined;
	let show = false;

	$: if (message != undefined) {
		show = true;
		setTimeout(() => {
			show = false;
			setTimeout(() => {
				message = undefined;
				code = undefined;
			}, 1000);
		}, 6000);
	}
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<!-- svelte-ignore a11y-mouse-events-have-key-events -->
<div
	class="popup valign radius-medium"
	class:show
	class:ok={code === 200}
	class:error={code !== 200}
	class:alert={code === 300}
	on:mouseover={() => {
		message = message;
	}}
>
	<i class="fa-solid" class:fa-circle-info={code === 200} class:fa-circle-exclamation={code !== 200}
	></i>
	{message}
	<!-- <button
		class="transparent"
		on:click={() => {
			show = false;
		}}><i class="fa-solid fa-arrow-right"></i></button
	> -->
</div>

<style>
	.popup {
		transition-duration: 2s !important;
		padding: 1rem;
		z-index: 10 !important;
		position: fixed;
		top: 1rem !important;
		right: -100% !important;
		gap: 1rem;
	}
	.show {
		right: 1rem !important;
	}
</style>
