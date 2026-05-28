import matplotlib.pyplot as plt

from autograd import grad, hessian, jacobian
import autograd.numpy as anp
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D


def main():
    fig, ax = plt.subplots()
    ax.plot([-1, 1], [-1, 1], label='$y-z=0$', linestyle='--', color='b')
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    x2d = anp.array([0.0, 0.0])
    x3d = anp.array([0., -0.7, 0.7])
    plt.close(fig)

    #newt, solutions, conv = newton_method_stop(x3d,  0.001, 100)
    gdsb, solutions, conv, alphas = gradient_descent_sb(x=x3d, max_iter=10, eta=0.0001)
    print(gdsb)
    #newt_SB, solutions, conv, alphas = newton_method_stop_SB(x3d,  0.001, 100)
    #print(newt_SB)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    g = np.linspace(-1.2, 1.2, 20)

    xx, yy = np.meshgrid(g, g)
    planes = [
        #(1, 0, 1, 1),    # x + z = 1
        #(0, 1, 1, 1),    # y + z = 1
        #(-1, 0, 1, 1),   # -x + z = 1
        #(0, -1, 1, 1),   # -y + z = 1
        #(1, 1, 1, 1.5),  # x + y + z = 1.5
        (0,1,-1,0),
        (1,0,-1,0)
    ]
    all_constraints = planes + [(1,0,0,1),(-1,0,0,1),(0,1,0,1),(0,-1,0,1)]
    for a1, a2, a3, b in planes:
        zz = np.clip((b - a1*xx - a2*yy) / a3, -2, 1.5)
        feasible = np.ones_like(zz, dtype=bool)
        for c1, c2, c3, cb in all_constraints:
            if (c1,c2,c3,cb) == (a1,a2,a3,b): continue
            feasible &= (c1*xx + c2*yy + c3*zz <= cb + 1e-6)
        zz_all = zz.copy()
        zz_feas = zz.copy()
        zz_feas[~feasible] = np.nan
        ax.plot_surface(xx, yy, zz_all, alpha=0.08, color='gray')
        ax.plot_surface(xx, yy, zz_feas, alpha=0.4)

    yy2, zz2 = np.meshgrid(g, g)
    ax.plot_surface( np.ones_like(yy2), yy2, zz2, alpha=0.2, color='cyan')
    ax.plot_surface(-np.ones_like(yy2), yy2, zz2, alpha=0.2, color='cyan')
    xx2, zz2 = np.meshgrid(g, g)
    ax.plot_surface(xx2,  np.ones_like(xx2), zz2, alpha=0.2, color='magenta')
    ax.plot_surface(xx2, -np.ones_like(xx2), zz2, alpha=0.2, color='magenta')
    xx3, yy3 = np.meshgrid(g, g)
    ax.plot_surface(xx3, yy3,  np.ones_like(xx3), alpha=0.2, color='yellow')
    ax.plot_surface(xx3, yy3, -np.ones_like(xx3), alpha=0.2, color='yellow')

    xs = [s[0] for s in solutions]
    ys = [s[1] for s in solutions]
    zs = [s[2] for s in solutions]
    ax.plot(xs, ys, zs, 'k.-', linewidth=0.5, markersize=5)
    ax.plot(x3d[0], x3d[1], x3d[2], 'ro')          # starting point
    ax.plot(gdsb[0], gdsb[1], gdsb[2], 'go') # result
    #ax.plot(newt_SB[0], newt_SB[1], newt_SB[2], 'go') # result

    """
    ax.plot(x2d[0], x2d[1], 'ro')
    ax.plot(x2d[0], x2d[1], 'ro')          # starting point
    ax.plot(newt[0], newt[1], 'go')    # result of gradient descent
    xs = [s[0] for s in solutions]
    ys = [s[1] for s in solutions]
    ax.plot(xs, ys, 'k.-', linewidth=0.5, markersize=5)  # path with points
    """
    """
    ax.plot(x_01[0], x_01[1], 'go')
    ax.plot(x_1[0], x_1[1], 'go')
    ax.plot(x_10[0], x_10[1], 'go')
    ax.plot(x_100[0], x_100[1], 'go')
    ax.plot(x_norm[0], x_norm[1], 'ro')
    """
   
    ax.set_title('Each solution for Gradient Descent with Line Search in 3d')
    #ax.set_title('Each solution for Newton Method with Line Search in 3d')
    plt.show()

    fig2, ax2 = plt.subplots()
    ax2.plot(alphas)
    ax2.set_xlabel('iteration')
    ax2.set_ylabel('step size α')
    ax2.set_title('Step size per iteration')
    #plt.show()

    fig2, ax2 = plt.subplots()
    ax2.plot(conv)
    ax2.set_xlabel('iteration')
    ax2.set_ylabel('objective fucntion')
    ax2.set_title('Convergence of the objective function in 3d')
    #plt.show()

def modify_point(x, count=1, gam=1, norm=False):
    i = 0
    while i < count:
        if norm==True:
            x = newton_method_norm(x, gam)
        else:
            x = newton_method_mod(x, gam)

        i += 1

    return x

def safe_log(v):
    return anp.log(anp.where(v > 0, v, 1e-300))

def obj_func(x, order=1):
    def f(x):
        return -(
            safe_log( -(x[0] * 1 + x[1] * 0 - 1) ) + 
            safe_log( -(x[0] * 0 + x[1] * 1 - 1) ) + 
            safe_log( -(x[0] * (-1) + x[1] * 0 - 1) ) + 
            safe_log( -(x[0] * 0 - x[1] * 1 - 1) ) + 
            safe_log( -(x[0] * 1 + x[1] * 1 - 1.5) )  
            )

    def slack(x):
        return anp.array(
            [(x[0] * 1 + x[1] * 0 - 1),
            (x[0] * 0 + x[1] * 1 - 1),
            (x[0] * (-1) + x[1] * 0 - 1),
            (x[0] * 0 - x[1] * 1 - 1), 
            (x[0] * 1 + x[1] * 1 - 1.5)]
        )

    match order:
        case 0:
            return slack(x), f(x)
        case 1:
            return slack(x), f(x), grad(f)(x)
        case 2:
            return slack(x), f(x), grad(f)(x), jacobian(grad(f))(x)
            
def obj_func_modified2d(x, order=1, gam=1):
    def f(x):
        return -(
            safe_log( -(x[0] * 1 + x[1] * 0 - 1) ) + 
            safe_log( -(x[0] * 0 + x[1] * 1 - 1) ) + 
            safe_log( -(x[0] * (-1) + x[1] * 0 - 1) ) + 
            safe_log( -(x[0] * 0 - x[1] * 1 - 1) ) + 
            safe_log( -(x[0] * (1*gam) + x[1] * (1*gam) - (1.5*gam)) )
            )
    def slack(x):
        return anp.array(
            [-(x[0] * 1 + x[1] * 0 - 1),
            -(x[0] * 0 + x[1] * 1 - 1),
            -(x[0] * (-1) + x[1] * 0 - 1),
            -(x[0] * 0 - x[1] * 1 - 1), 
            -(x[0] * (1*gam) + x[1] * (1*gam) - (1*gam))]
        )

    match order:
        case 0:
            return slack(x), f(x)
        case 1:
            return slack(x), f(x), grad(f)(x)
        case 2:
            return slack(x), f(x), grad(f)(x), jacobian(grad(f))(x)


def obj_func_modified3d(x, order=1):
    def f(x):
        return -(
            safe_log(-(x[1] - x[2])) +                   # y + z <= 0
            safe_log(-(x[0] - x[2])) +                   # x + z <= 0 
            safe_log(x[0] + 1) + safe_log(1 - x[0]) +    # -1 <= x <= 1
            safe_log(x[1] + 1) + safe_log(1 - x[1]) +    # -1 <= y <= 1
            safe_log(x[2] + 1) + safe_log(1 - x[2])      # -1 <= z <= 1
        )
    def slack(x):
        return anp.array([-(x[1] - x[2])])

    match order:
        case 0:
            return slack(x), f(x)
        case 1:
            return slack(x), f(x), grad(f)(x)
        case 2:
            return slack(x), f(x), grad(f)(x), jacobian(grad(f))(x)


def obj_func_normalized(x, order=1, gam=1):
    def f(x):
        return -(
            anp.log( -(x[0] * 1 + x[1] * 0 - 1) ) + 
            anp.log( -(x[0] * 0 + x[1] * 1 - 1) ) + 
            anp.log( -(x[0] * (-1) + x[1] * 0 - 1) ) + 
            anp.log( -(x[0] * 0 - x[1] * 1 - 1) ) + 
            anp.log( -(x[0] * (1*gam) + x[1] * (1*gam) - (1*gam)) )  
            )
    def slack(x):
        return anp.array(
            [-(x[0] * 1 + x[1] * 0 - 1),
            -(x[0] * 0 + x[1] * 1 - 1),
            -(x[0] * (-1) + x[1] * 0 - 1),
            -(x[0] * 0 - x[1] * 1 - 1), 
            -(x[0] * (gam*1) + x[1] * (1*gam) - 1)]
        )

    match order:
        case 0:
            return slack(x), f(x)
        case 1:
            return slack(x), f(x), grad(f)(x)
        case 2:
            return slack(x), f(x), grad(f)(x), jacobian(grad(f))(x)


def newton_method(x):
    _, _, grad, hes = obj_func(x, order=2)
    return x - anp.linalg.inv(hes) @ grad

def newton_method_stop(x, crit, max_iter, gam=1, alpha=1, beta=1e-4, sigma=0.5):
    i = 0
    solutions = []
    convergence = []
    while i < max_iter :

        _, _, grad, hes = obj_func_modified2d(x, order=2)
        x_new = x - anp.linalg.inv(hes) @ grad
        solutions.append(x_new)
        convergence.append(obj_func_modified3d(x_new, order=1)[1])
        if math.dist(x_new, x) <= crit:
            return x_new, solutions, convergence
        x = x_new
        i += 1
    return x, solutions, convergence

def newton_method_stop_SB(x, crit, max_iter, alpha=1, beta=1e-4, sigma=0.5):
    i = 0
    solutions = []
    convergence = []
    steps = []
    while i < max_iter :
        def f(v):
            return obj_func_modified3d(v, order=1)[1]
        nabla = grad(f)
        _, _, g, hes = obj_func_modified3d(x, order=2)
        val = f(x)
        step_size = strong_bracketing(x, f, nabla, d=-g, y0=val, g0_vec=g, alpha=alpha, beta=beta, sigma=sigma)
        steps.append(step_size)
        x_new = x - step_size * anp.linalg.inv(hes) @ g
        solutions.append(x_new)
        convergence.append(f(x_new))
        if math.dist(x_new, x) <= crit:
            return x_new, solutions, convergence, steps
        x = x_new
        i += 1
    return x, solutions, convergence, steps

def newton_method_mod(x, gam=1):
    _, _, grad, hes = obj_func_modified(x, order=2, gam=gam)
    
    return x - anp.linalg.inv(hes) @ grad

def newton_method_norm(x, gam=1):
    _, _, grad, hes = obj_func_normalized(x, order=2, gam=gam)
    return x - anp.linalg.inv(hes) @ grad

def gradient_descent_sb(x, max_iter, eta=1e-6, alpha=1, beta=1e-4, sigma=0.5):
    def f(v):
        return obj_func_modified3d(v, order=1)[1]
    nabla = grad(f)
    convergence = []
    solutions = []
    alphas = []

    for _ in range(max_iter):

        val = f(x)
        g = nabla(x)
        convergence.append(val)
        solutions.append(x)

        # stopping criterion
        if anp.linalg.norm(g) <= eta:
            break

        # search direction
        d = -g

        # line search
        alpha_k = strong_bracketing(x, f, nabla, d=d, y0=val, g0_vec=g, alpha=alpha, beta=beta, sigma=sigma)

        # ensure feasibility
        x_new = x + alpha_k * d
        x_new = anp.clip(x_new, -1 + 1e-8, 1 - 1e-8)

        alphas.append(alpha_k)
        x = x_new

    return x, solutions, convergence, alphas


def strong_bracketing(x, f, nabla, d, y0, g0_vec, alpha=1, beta=1e-4, sigma=1):
        g0 = g0_vec @ d
        y_prev, alpha_prev = None, 0

        # bracket phase
        while True:
            y = f(x + alpha*d)
            if y > y0 + beta*alpha*g0 or (y_prev is not None and y >= y_prev):
                alpha_lo, alpha_hi = alpha_prev, alpha
                break
            dir_gradient = nabla(x + alpha*d) @ d
            if abs(dir_gradient) <= sigma * abs(g0):
                return alpha
            elif dir_gradient >= 0:
                alpha_lo, alpha_hi = alpha, alpha_prev
                break
            else:
                pass
            y_prev, alpha_prev, alpha = y, alpha, 1.5 * alpha

        # zoom phase
        ylo = f(x + alpha_lo*d)
        while abs(alpha_hi - alpha_lo) > 1e-6:
            alpha = (alpha_lo + alpha_hi)/2
            y = f(x + alpha*d)
            if y > y0 + beta*alpha*g0 or y >= ylo:
                alpha_hi = alpha
            else:
                g = nabla(x + alpha*d) @ d
                if abs(g) <= sigma*abs(g0):
                    return alpha
                elif g*(alpha_hi - alpha_lo) >= 0:
                    alpha_hi = alpha_lo
                else:
                    pass
                alpha_lo = alpha
        return alpha_lo

if __name__ == "__main__":
    main()
