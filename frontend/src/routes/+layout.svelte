<script lang="ts">
	import { isUserLogged } from '$lib/stores.js';
	import '../app.css';
	import '@fortawesome/fontawesome-free/css/all.min.css';
	import { setTheme, currentTheme } from '$lib/theme';
	export let data;

	async function logout() {
		const response = await fetch('/auth/logout');

		if (response.ok) {
			isUserLogged.set(false);
		} else {
			console.error('Logout failed');
		}
	}
	isUserLogged.set(data.user?.loggedIn);
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<nav>
	<div class="left">
		<a href="/">Home<span class="hide2"></span></a>
		|
		<a href="/">WIP<span class="hide2"></span></a>
		|
		<a href="https://github.com/SalaniLeo/PhotoGallery"
			><i class="fa-brands fa-github"></i><span class="hide2"></span></a
		>
	</div>
	<div class="center"></div>
	<div class="right">
		<div class="user-management">
			{#if $isUserLogged == true}
				<a href="/auth/login" on:click={logout}
					>Log Out <span class="hide2"><i class="fa-solid fa-right-from-bracket"></i></span></a
				>
			{:else if $isUserLogged == false}
				<a href="/auth/login"
					>Log In <span class="hide2"><i class="fa-solid fa-right-to-bracket"></i></span></a
				>
			{/if}
		</div>
		<div id="theme-select">
			{#if $currentTheme == 'dark'}
				<i class="fa-regular fa-sun themer" on:click={() => setTheme('light', true)}></i>
			{:else}
				<i class="fa-regular fa-moon themer" on:click={() => setTheme('dark', true)}></i>
			{/if}
		</div>
	</div>
</nav>
<slot />
<footer>Every image is free of charge and can be used in any desired way</footer>

<style>
	footer {
		padding: 1rem;
		text-align: center;
		color: var(--outline-inactive);
	}
	nav {
		color: var(--text-color);
		display: grid;
		grid-template-columns: 1fr 1fr 1fr;
		background-color: var(--accent-color-primary);
		margin-top: 1rem;
		margin-bottom: 1rem;
		margin-left: 12rem;
		margin-right: 12rem;
		padding: 1rem;
		border-radius: 10px;
		box-shadow: var(--shadow-color-heavy) 0px 0px 10px;
		text-align: center;
		align-items: center;
	}

	nav > .left {
		display: flex;
		justify-content: flex-start;
		gap: 10px;
		align-items: center;
	}

	nav > .center {
		display: flex;
		justify-content: center;
		gap: 10px;
		align-items: center;
	}

	nav > .right {
		display: flex;
		justify-content: flex-end;
		gap: 10px;
		align-items: center;
	}

	nav * {
		min-width: max-content;
	}

	.themer {
		scale: 115%;
		display: flex;
		align-items: center;
		width: 20px;
		cursor: pointer;
	}

	@media screen and (max-width: 1200px) {
		nav {
			margin-left: 8rem;
			margin-right: 8rem;
		}
	}
	@media screen and (max-width: 1000px) {
		nav {
			margin-left: 4rem;
			margin-right: 4rem;
		}
		nav .hide2 {
			display: none;
		}
	}
	@media screen and (max-width: 720px) {
		nav {
			margin-left: 0rem;
			margin-right: 0rem;
			margin-top: 0rem;
			border-radius: 0px;
			grid-template-columns: 0.5fr 2fr 0.5fr;
		}
		/* nav .hide1 {
			display: none;
		} */
	}
</style>
