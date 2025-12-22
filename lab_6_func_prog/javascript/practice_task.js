const users = require('./users.json');

const processUsers = (users) => {
    let average_age = users.map(user => user["age"])
                          .reduce((sum, age) => sum + age, 0) / users.length;
    
    let cities = {};
    for (let user of users) {
        const city = user.city;
        if (!cities[city]) {
            cities[city] = [];
        }
        cities[city].push(user);
    }
    
    let cities_counted = Object.keys(cities).map(city => {
        return { [city]: cities[city].length };
    });
    

    let actives = users.filter(user => user['isActive'] === true)
                      .map(user => user["email"]);

    return {
        "Средний возраст пользователей": average_age,
        "Количество пользователей по городу": cities_counted,
        "Список email активных пользователей": actives
    };
};

import { useState, useCallback } from 'react';

const useForm = (initialValues = {}, validators = {}) => {
    const [values, setValues] = useState(initialValues);
    const [errors, setErrors] = useState({});
    const [touched, setTouched] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleChange = useCallback((fieldName) => (event) => {
        const value = event.target.type === 'checkbox' 
            ? event.target.checked 
            : event.target.value;
        
        setValues(prev => ({ ...prev, [fieldName]: value }));
        setTouched(prev => ({ ...prev, [fieldName]: true }));
        
        if (validators[fieldName]) {
            const error = validators[fieldName](value, values);
            setErrors(prev => ({
                ...prev,
                [fieldName]: error
            }));
        }
    }, [validators, values]);

    const resetForm = useCallback(() => {
        setValues(initialValues);
        setErrors({});
        setTouched({});
        setIsSubmitting(false);
    }, [initialValues]);

    const setFieldValue = useCallback((fieldName, value) => {
        setValues(prev => ({ ...prev, [fieldName]: value }));
        setTouched(prev => ({ ...prev, [fieldName]: true }));
    }, []);

    const validateForm = useCallback(() => {
        const newErrors = {};
        let isValid = true;

        Object.keys(validators).forEach(fieldName => {
            const validator = validators[fieldName];
            if (validator) {
                const error = validator(values[fieldName], values);
                if (error) {
                    newErrors[fieldName] = error;
                    isValid = false;
                }
            }
        });

        setErrors(newErrors);
        setTouched(
            Object.keys(values).reduce((acc, key) => ({ ...acc, [key]: true }), {})
        );
        
        return isValid;
    }, [validators, values]);

    const handleSubmit = useCallback((onSubmit) => async (event) => {
        if (event) {
            event.preventDefault();
            event.persist();
        }

        setIsSubmitting(true);
        
        const isValid = validateForm();
        
        if (isValid) {
            try {
                await onSubmit(values, { resetForm, setErrors });
            } catch (error) {
                console.error('Form submission error:', error);
                // Можно установить общую ошибку формы
                setErrors(prev => ({
                    ...prev,
                    _form: error.message || 'Ошибка отправки формы'
                }));
            }
        }
        
        setIsSubmitting(false);
    }, [values, validateForm, resetForm]);

    const hasErrors = Object.keys(errors).some(key => errors[key] && touched[key]);

    return {
        values,
        errors,
        touched,
        isSubmitting,
        isValid: !hasErrors,
        
        handleChange,
        handleSubmit,
        resetForm,
        setFieldValue,
        
        getFieldProps: (fieldName) => ({
            name: fieldName,
            value: values[fieldName] || '',
            onChange: handleChange(fieldName),
            onBlur: () => setTouched(prev => ({ ...prev, [fieldName]: true })),
            error: touched[fieldName] && errors[fieldName],
            helperText: touched[fieldName] && errors[fieldName]
        }),
        
        getFieldError: (fieldName) => touched[fieldName] ? errors[fieldName] : undefined
    };
};

const debounce = (func, delay, options = {}) => {
    let timeoutId = null;
    let lastArgs = null;
    let lastCallTime = 0;
    let lastInvokeTime = 0;
    
    const { leading = false, maxWait } = options;
    const maxWaitDelay = maxWait || null;

    const clearTimer = () => {
        if (timeoutId) {
            clearTimeout(timeoutId);
            timeoutId = null;
        }
    };

    const timerExpired = () => {
        const time = Date.now();
        
        const canInvoke = !leading || (time - lastCallTime) >= delay;
        
        if (canInvoke) {
            invokeFunc();
            return;
        }
        
        const timeSinceLastCall = time - lastCallTime;
        const timeSinceLastInvoke = time - lastInvokeTime;
        const timeWaiting = delay - timeSinceLastCall;
        
        if (maxWaitDelay !== null) {
            const remainingWait = Math.max(timeWaiting, maxWaitDelay - timeSinceLastInvoke);
            timeoutId = setTimeout(timerExpired, remainingWait);
        } else {
            timeoutId = setTimeout(timerExpired, timeWaiting);
        }
    };

    const invokeFunc = () => {
        if (lastArgs === null) return;
        
        func.apply(this, lastArgs);
        lastArgs = null;
        lastInvokeTime = Date.now();
    };

    const debounced = function(...args) {
        const time = Date.now();
        const isInvoking = leading && timeoutId === null;
        
        lastArgs = args;
        lastCallTime = time;
        
        if (isInvoking) {
            lastInvokeTime = time;
            func.apply(this, args);
        }
        
        clearTimer();
        
        if (maxWaitDelay !== null && !timeoutId && !isInvoking) {
            timeoutId = setTimeout(timerExpired, maxWaitDelay);
        } else {
            timeoutId = setTimeout(timerExpired, delay);
        }
    };

    debounced.cancel = () => {
        clearTimer();
        lastArgs = null;
        lastCallTime = 0;
        lastInvokeTime = 0;
    };

    debounced.flush = () => {
        if (timeoutId) {
            clearTimer();
            invokeFunc();
        }
    };

    debounced.pending = () => {
        return timeoutId !== null;
    };

    return debounced;
};

const simpleDebounce = (func, delay) => {
    let timeoutId;
    
    return function(...args) {
        const context = this;
        
        clearTimeout(timeoutId);
        
        timeoutId = setTimeout(() => {
            func.apply(context, args);
        }, delay);
    };
};

const debounceImmediate = (func, delay, immediate = false) => {
    let timeoutId;
    
    return function(...args) {
        const context = this;
        const callNow = immediate && !timeoutId;
        
        const later = () => {
            timeoutId = null;
            if (!immediate) {
                func.apply(context, args);
            }
        };
        
        clearTimeout(timeoutId);
        timeoutId = setTimeout(later, delay);
        
        if (callNow) {
            func.apply(context, args);
        }
    };
};

export default debounce;
export { simpleDebounce, debounceImmediate };