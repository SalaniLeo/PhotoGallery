<script lang="ts">
	import { isUserLogged } from '$lib/stores.js';
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
	isUserLogged.set(data.user.loggedIn);
</script>

<nav>
	<div class="left">
		<a href="/">Home<span class="hide2"></span></a>
		|
		<a href="/gallery">Gallery<span class="hide2"></span></a>
		{#if data.user.loggedIn}
			|
			<a href="/statistics">Statistics<span class="hide2"></span></a>
		{/if}
	</div>
	<div class="center"></div>
	<div class="right">
		<div class="user-management">
			{#if $isUserLogged == true}
				<a href="/profile">Profile</a>
			{:else if $isUserLogged == false}
				<a href="/auth/login"
					>Log In <span class="hide2"><i class="fa-solid fa-right-to-bracket"></i></span></a
				>
			{/if}
		</div>
		|
		<div id="theme-select">
			<!-- svelte-ignore a11y-no-static-element-interactions -->
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			{#if $currentTheme == 'dark'}
				<i class="fa-regular fa-sun themer" on:click={() => setTheme('light', true)}></i>
			{:else}
				<i class="fa-regular fa-moon themer" on:click={() => setTheme('dark', true)}></i>
			{/if}
		</div>
	</div>
</nav>

<style>
	nav {
		color: var(--text-color);
		display: grid;
		grid-template-columns: 1fr 1fr 1fr;
		background-color: var(--background-blurry);
		backdrop-filter: blur(10px);
		margin-top: 1rem;
		margin-bottom: 1rem;
		margin-left: 12rem;
		margin-right: 12rem;
		padding: 1rem;
		border-radius: 10px;
		text-align: center;
		align-items: center;
		justify-content: center;
		border: 2px solid var(--border-color);
	}

	nav > .left {
		display: flex;
		justify-content: flex-start;
		gap: 0.5rem;
		align-items: bottom;
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
			border: none;
			height: 32px;
			border-bottom: 2px solid var(--border-color);
		}
	}
</style>
